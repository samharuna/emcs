from django.contrib import admin
from applications.models import Loan, LoanDuration, Investment,  InvestmentDuration, Requirement
# Register your models here.

admin.site.register(Loan)
admin.site.register(LoanDuration)
admin.site.register(Investment)
admin.site.register(InvestmentDuration)
admin.site.register(Requirement)

