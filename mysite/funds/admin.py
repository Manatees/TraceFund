from django.contrib import admin

from .models import Fund, FundHistory, RedemptionRateTable, PruchaseTrade

class FundAdmin(admin.ModelAdmin):
	list_display = ('fund_name', 'fund_code', 'fund_p_rate')


class FundHistoryAdmin(admin.ModelAdmin):
	list_display = ('fund', 'date', 'netprice')

class RedemptionRateTableAdmin(admin.ModelAdmin):
	list_display = ('fund', 'days', 'rate_value')

class PruchaseTradeAdmin(admin.ModelAdmin):
	list_display = ('fund', 'purchase_date', 'amount', 'ack_amount', 'netprice', 'holdon_shares')	

admin.site.register(Fund, FundAdmin)
admin.site.register(FundHistory, FundHistoryAdmin)
admin.site.register(RedemptionRateTable, RedemptionRateTableAdmin)
admin.site.register(PruchaseTrade, PruchaseTradeAdmin)