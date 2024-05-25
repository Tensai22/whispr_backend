from django.urls import path
from .views import ItemListCreate, UserListCreate

urlpatterns = [
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
]
