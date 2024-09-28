from django.urls import path
from .views import add_income, add_expense,dashboard

app_name = 'tracking'

urlpatterns = [
    path('addincome/', add_income, name='add_income'),
    path('addexpense/', add_expense, name='add_expense'),
    path('',dashboard,name="dashboard"),
]
