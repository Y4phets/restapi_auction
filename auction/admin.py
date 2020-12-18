from django.contrib import admin
from .models import Auction, Bid


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    """Аукцион"""
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Ставка"""
    list_display = ("auction_id", "user_id", "rate", "bid_time",)
    list_display_links = ("auction_id", "user_id", "rate",)
