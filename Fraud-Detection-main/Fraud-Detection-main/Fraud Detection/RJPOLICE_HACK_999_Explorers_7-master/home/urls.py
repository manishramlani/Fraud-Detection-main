from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("", views.index, name='home'),
    path("login", views.loggin, name='login'),
    path('register', views.register, name='register'),
    path('transfer', views.transfer,name='transfer'),
    path('transaction_success', views.transfer,name='transaction_success'),
    path('suspicious_transaction', views.transfer,name='suspicious_transaction'),
    path('history', views.history, name='history'),
    
    
]