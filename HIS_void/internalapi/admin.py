from django.contrib import admin

from internalapi.models import PaymentRecord


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "trade_no", "total_amount", "timestamp", 
        "item_type", "item_name", "item_pk",
        "is_pay",
    )
    list_filter = ("item_type", "is_pay",)
    search_fields = ("trade_no", "timestamp", "item_name", "item_pk")
