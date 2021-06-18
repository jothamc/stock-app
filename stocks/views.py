from django.http.response import JsonResponse
from rest_framework.views import APIView
from .serializers import StocksSerializer
from django.shortcuts import render
from django.views import View

from .utils import StockLoader

from django.utils import timezone

from .models import Stocks

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
# Create your views here.

class LoadStockView(View):

    def get(self, request):

        return render(request, 'stocks/load-stocks.html')

    def post(self, request):

        date = request.POST.get('date')

        datetime = timezone.datetime.fromisoformat(date)

        day = datetime.day
        month = datetime.month
        year = datetime.year

        StockLoader().load_stocks(year, month, day)

        return render(request, 'stocks/load-stocks.html')


class StockViewSet(ModelViewSet):

    queryset = Stocks.objects.filter(symbol="AMBER")
    serializer_class = StocksSerializer


class SymbolView(View):

    def get(self,request):

        symbols = []

        for stock in Stocks.objects.all():
            if stock.symbol not in symbols:
                symbols.append(stock.symbol)

        return JsonResponse({'symbols': symbols})


class StockDetailView(APIView):

    def post(self, request):

        symbol = request.data.get('symbol')
        date = request.data.get('date')

        stocks = Stocks.objects.filter(symbol=symbol, date__gte=date)

        serializer = StocksSerializer(stocks, many=True)

        return Response(serializer.data)
