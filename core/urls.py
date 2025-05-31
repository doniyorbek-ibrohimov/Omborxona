
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='index'),
    path('mahsulotlar/',ProductView.as_view(),name='mahsulotlar'),
    path('mijozlar/',ClientView.as_view(),name='mijozlar'),
    path('stats/',RecordView.as_view(),name='stats'),
    path('stats/<int:pk>/update/',RecordUpdate.as_view(),name='stats-update'),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(),name='product_update'),
    path('clients/<int:pk>/update/',ClientUpdateView.as_view(),name='client_update'),
]
urlpatterns+=[
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView,name="logout")
]
