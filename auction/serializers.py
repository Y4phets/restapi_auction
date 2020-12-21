from rest_framework import serializers

from .models import Auction, Bid


class AuctionSerializer(serializers.ModelSerializer):
    """Список аукционов"""

    class Meta:
        model = Auction
        fields = ("id", "name", "description", "expiration_date", "initial_rate",)


class AuctionDetailSerializer(serializers.ModelSerializer):
    """Аукцион"""

    class Meta:
        model = Auction
        fields = ("name", "description", "initial_rate",)


class BidCreateSerializer(serializers.ModelSerializer):
    """Создание ставки"""

    class Meta:
        model = Bid
        fields = ("user", "auction", "bid_time", "rate",)
