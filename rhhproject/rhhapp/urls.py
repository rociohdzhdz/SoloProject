from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('newuser', views.newuser),
    path('userexist', views.userexist),
    path('userhome/<int:id>', views.userhome),
    path('storehome/<int:id>', views.storehome),
    path('loginuser', views.loginuser),
    path('myaccount/<int:id>', views.myaccount),
    path('newreceipt', views.newreceipt),
    path('newreceiptstore', views.newreceiptstore),
    path('searchreceiptstore', views.searchreceiptstore),
    path('delete/<int:id>', views.delete),
    path('logout', views.logout),
]