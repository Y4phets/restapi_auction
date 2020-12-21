from rest_framework import serializers

from .models import Auction, Bid


class AuctionSerializer(serializers.ModelSerializer):
    """Список аукционов"""

    class Meta:
        model = Auction
        fields = ("id", "name", "description", "expiration_date", "initial_rate",)


class AuctionDetailFinishedSerializer(serializers.ModelSerializer):
    """Просмотр завершённых аукционов"""
    winner_name = serializers.SerializerMethodField()
    winner_email = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ("finish_rate", "winner_name", "winner_email",)

    def get_winner_name(self, obj):
        return obj.winner.username

    def get_winner_email(self, obj):
        return obj.winner.email


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
