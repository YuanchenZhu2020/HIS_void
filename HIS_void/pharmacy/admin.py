from django.contrib import admin

from pharmacy.models import MedicineInfo, MedicinePurchase


@admin.register(MedicineInfo)
class MedicineInfoAdmin(admin.ModelAdmin):
    list_display = (
        "medicine_id", "medicine_name",
        "content_spec", "package_spec",
        "cost_price", "retail_price",
        "stock_num", "shelf_day",
        "special", "OTC"
    )
    list_filter = ("medicine_id", "medicine_name", )
    search_fields = ("medicine_id", "medicine_name", "shelf_day", )


@admin.register(MedicinePurchase)
class MedicinePurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "medicine_info", "batch_num", "purchase_date", "purchase_quantity",
    )
    list_filter = ("medicine_info", "purchase_date", )
    search_fields = ("medicine_info", "purchase_date", )
