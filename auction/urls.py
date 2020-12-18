from django.urls import path, include
from rest_framework import routers

from .views import AuctionView, BidView

router = routers.DefaultRouter()
router.register(r"auction", AuctionView, basename="auction")
urlpatterns = [
    path('', include(router.urls)),
    path('bid/', BidView.as_view()),
]
