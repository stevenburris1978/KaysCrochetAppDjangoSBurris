from django.contrib import admin

from .models import Choice, Item


admin.site.site_header = "Kay's Crochet Administration"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["item_title", "description", "image"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["item_title", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["item_title"]


admin.site.register(Choice)
admin.site.register(Item, ItemAdmin)
