from django.contrib import admin

from pharmacy.models import MedicineInfo, MedicinePurchase


class MedicineInfoAdmin(admin.ModelAdmin):
    list_display = (
        "medicine_id", "batch_num", "medicine_name", 
        "cost_price", "retail_price", 
        "stock_num", "overdue_date"
    )
    list_filter = ("medicine_id", "batch_num", "medicine_name", )
    search_fields = ("medicine_id", "batch_num", "medicine_name", )

admin.site.register(MedicineInfo, MedicineInfoAdmin)
