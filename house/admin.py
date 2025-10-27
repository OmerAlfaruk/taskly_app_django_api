from django.contrib import admin
from .models import House

class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    readonly_fields=('id','created_at')
    search_fields = ('name', 'manager__username')


admin.site.register(House)

