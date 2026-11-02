from django.urls import path
from .views import EtractData

urlpatterns=[
    path('',EtractData.as_view(),name='data')
]