from .models import Customer
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'account_number', 'amount', 'pin')
    search_fields = ('full_name', 'account_number')


admin.site.register(Customer, CustomerAdmin)
