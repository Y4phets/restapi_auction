from django.contrib.auth.models import User
from django.db import models


class Auction(models.Model):
    """Аукцион"""
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    active = models.BooleanField(default=False, verbose_name="")
    initial_rate = models.PositiveIntegerField("Начальная ставка", default=0,
                                               help_text="указывать сумму в долларах")
    finish_rate = models.PositiveIntegerField("Конечная ставка", default=0,
                                              help_text="указывать сумму в долларах")
    expiration_date = models.DateTimeField("Дата завершения", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    winner = models.ForeignKey(User, verbose_name="Победитель", on_delete=models.CASCADE, related_name="bid_winner")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аукцион"
        verbose_name_plural = "Аукцион"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveIntegerField("Cтавка", default=0,
                                       help_text="указывать сумму в долларах")

    def __str__(self):
        return "USER:" + str(self.user.name) + " AUCTION:" + \
               str(self.auction.name) + " " + str(self.bid_time)
