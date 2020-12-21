from django.urls import path, include
from rest_framework import routers

from .views import AuctionView, BidView, AuctionDetailFinishedView

router = routers.DefaultRouter()
router.register(r"auction", AuctionView, basename="auction")
urlpatterns = [
    path('', include(router.urls)),
    path('bid/', BidView.as_view()),
    path('finished/<int:pk>/', AuctionDetailFinishedView.as_view({'get': 'retrieve'})),
]
