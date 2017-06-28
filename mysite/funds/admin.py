from django.contrib import admin

from .models import Fund, FundHistory, RedemptionRateTable

class FundAdmin(admin.ModelAdmin):
	list_display = ('fund_name', 'fund_code', 'fund_p_rate')


class FundHistoryAdmin(admin.ModelAdmin):
	list_display = ('fund', 'date', 'netprice')

class RedemptionRateTableAdmin(admin.ModelAdmin):
	list_display = ('fund', 'days', 'rate_value')

	
admin.site.register(Fund, FundAdmin)
admin.site.register(FundHistory, FundHistoryAdmin)
admin.site.register(RedemptionRateTable, RedemptionRateTableAdmin)
