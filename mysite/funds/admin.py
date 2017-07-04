# coding=utf-8
from django.contrib import admin

from .models import Fund, FundHistory, RedemptionRateTable, PruchaseTrade, RedemptionTrade

class FundAdmin(admin.ModelAdmin):
	list_display = ('fund_name', 'fund_code', 'fund_p_rate')


class FundHistoryAdmin(admin.ModelAdmin):
	list_display = ('fund', 'date', 'netprice')

class RedemptionRateTableAdmin(admin.ModelAdmin):
	list_display = ('fund', 'days', 'rate_value')

class PruchaseTradeAdmin(admin.ModelAdmin):
	list_display = ('fund', 'purchase_date', 'amount', 'ack_amount', 'netprice', 'holdon_shares')	

class RedemptionTradeAdmin(admin.ModelAdmin):
	list_display = ('fund', 'redemption_date', 'redemption_share_amount', 'benefit_amount')

admin.site.register(Fund, FundAdmin)
admin.site.register(FundHistory, FundHistoryAdmin)
admin.site.register(RedemptionRateTable, RedemptionRateTableAdmin)
admin.site.register(PruchaseTrade, PruchaseTradeAdmin)
admin.site.register(RedemptionTrade, RedemptionTradeAdmin)