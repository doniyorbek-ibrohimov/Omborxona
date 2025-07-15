from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_obtain_pair,token_refresh

from main.views import *

router=DefaultRouter()
router.register('products',ProductViewSet)
router.register('clients',ClientViewSet)
router.register('records',RecordViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),

]
urlpatterns+=[
    path('token',token_obtain_pair),
    path('token-refresh',token_refresh),
    path('register/',RegisterCreateAPIView.as_view()),
]
