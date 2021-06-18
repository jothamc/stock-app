
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Stocks


class StocksSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = Stocks
        fields = ['close', 'date', 'high', 'low', 'open_price']