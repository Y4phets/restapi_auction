from datetime import datetime, timedelta
import logging
from django.utils.timezone import utc
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Auction, Bid
from .serializers import AuctionSerializer, AuctionDetailSerializer, BidCreateSerializer

logger = logging.getLogger("Auction")


class AuctionView(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("name", "active", "expiration_date")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuctionDetailSerializer
        else:
            return AuctionSerializer

    def get_queryset(self):
        auctions = Auction.objects.all().order_by("-expiration_date")
        return auctions

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Update available to the author of the auction")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        auction = Auction.objects.get(id=kwargs["pk"])

        if request.user != auction.author:
            return Response(data={'results': "Update available to the author of the auction"},
                            status=HTTP_403_FORBIDDEN)

        return self.update(request, *args, **kwargs)


class BidView(generics.CreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("user_id", "auction_id", "bid_time")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BidCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auction = Auction.objects.get(pk=serializer.data["auction_id"])
        now = datetime.utcnow().replace(tzinfo=utc)

        if auction.expiration_date < now:
            return Response(data={'results': "Time is over"},
                            status=HTTP_403_FORBIDDEN)

        elif (auction.expiration_date - now).seconds <= 60:
            auction.expiration_date += timedelta(minutes=2)
            auction.save()

        latest_bid = Bid.objects.filter(auction_id=auction.id).order_by('bid_time').last()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
