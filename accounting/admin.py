from django.contrib import admin
from .models import Customers, Accounts, Transactions, Transfers

admin.site.register(Customers)
admin.site.register(Accounts)
admin.site.register(Transactions)
admin.site.register(Transfers)