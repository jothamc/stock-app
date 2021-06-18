from django.contrib import admin
from .models import Stocks
# Register your models here.

@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    '''Admin View for Stocks'''

    list_display = ('symbol', 'high', 'low', 'close', 'date')
    list_filter = ('date',)
    ordering = ('symbol',)