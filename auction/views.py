import logging
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils.timezone import utc
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from .models import Auction, Bid
from .serializers import AuctionSerializer, AuctionDetailSerializer, BidCreateSerializer, \
    AuctionDetailFinishedSerializer

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


class AuctionDetailFinishedView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuctionDetailFinishedSerializer
    queryset = Auction.objects.filter(active=False)

    def retrieve(self, request, pk=None):
        auction = get_object_or_404(self.queryset, pk=pk)
        serializer = AuctionDetailFinishedView(auction)
        return Response(serializer.data)


class BidView(generics.CreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("user", "auction", "bid_time")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BidCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        rate = data["rate"]

        auction = Auction.objects.get(pk=data["auction"])
        latest_bid = Bid.objects.filter(auction_id=auction.id).order_by('bid_time').last()

        now = datetime.utcnow().replace(tzinfo=utc)

        if auction.expiration_date < now:
            return Response(data={'results': "Time is over"},
                            status=HTTP_400_BAD_REQUEST)

        elif (auction.expiration_date - now).seconds <= 60:
            auction.expiration_date += timedelta(minutes=2)
            auction.save()

        if latest_bid.rate > rate:
            return Response(data={'results': "Rate lower than current"},
                            status=HTTP_400_BAD_REQUEST)
        else:
            auction.winner = User.objects.get(id=data["user"])
            auction.finish_rate = rate
            auction.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
