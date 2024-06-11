

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('customer', views.CustomerViewSet, basename='customer')
router.register('account', views.AccountViewSet, basename='account')
router.register('action', views.ActionViewSet, basename='action')
router.register('transaktion', views.TransaktionViewSet, basename='transaktion')
router.register('transfer', views.TransferViewSet, basename='transfer')

urlpatterns = [
    #path('customer-list/', views.CustomerList.as_view(), name='customer-list'),
    #path('customer-detail/<ink:pk/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('', include(router.urls))
]
