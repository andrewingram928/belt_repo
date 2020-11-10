from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('log_out', views.logout),
    path('edit_account', views.edit_account),
    path('users/<int:user_id>', views.user_profile),
    path('quotes', views.quotes),
    path('quotes/add', views.add_quote),
    path('quotes/delete/<int:quote_id>', views.delete_quote),
    path('quotes/like/<int:quote_id>', views.like_quote),
]