from django.urls import path
from .views import create_account, create_category, create_transaction ,dashboard
from .views import delete_transaction
app_name = 'tracking'
urlpatterns = [
    path('createAccount/', create_account, name='createAccount'),
    path('createCategory', create_category, name='createCategory'),
    path('createTransaction', create_transaction, name='createTransaction'),
    path('', dashboard, name="dashboard"),
    path('deleteTransaction/<int:pk>', delete_transaction, name='deleteTransaction'),
   

]
