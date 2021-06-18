from django.db import models

# Create your models here.
class Stocks(models.Model):

    date = models.DateField()
    high = models.FloatField()
    low = models.FloatField()
    open_price = models.FloatField()
    close = models.FloatField()
    symbol = models.CharField(max_length=40)