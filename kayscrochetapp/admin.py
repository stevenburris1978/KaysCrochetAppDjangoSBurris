from django.contrib import admin
from .models import Choice, Item, LikeItem, Customerorder


admin.site.site_header = "Kay's Crochet Administration"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["item_title", "description", "image", "image2", "image3", "image4", "price"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["item_title", "description", "price", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["item_title"]


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'street', 'city', 'state', 'zip_code', 'total_price', 'item_title')


admin.site.register(Choice)
admin.site.register(Item, ItemAdmin)
admin.site.register(LikeItem)
admin.site.register(Customerorder, CustomerOrderAdmin)
