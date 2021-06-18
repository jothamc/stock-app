from .views import LoadStockView, StockDetailView, SymbolView
from django.urls import path


urlpatterns = [
    path('load/', LoadStockView.as_view(), name=''),
    path('symbols/', SymbolView.as_view(), name=''),
    path('get-stocks/', StockDetailView.as_view(), name=''),
]