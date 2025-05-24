
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',BranchView.as_view(),name='bolimlar'),
    path('mahsulotlar/',ProductView.as_view(),name='mahsulotlar'),
    path('mijozlar/',ClientView.as_view(),name='mijozlar'),
    path('stats/',RecordView.as_view(),name='stats'),
]
urlpatterns+=[
    path('logout/',LogoutView,name="logout")
]
