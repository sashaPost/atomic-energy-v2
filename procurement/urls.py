from django.urls import path
from .api import ProcurementsAPIView



urlpatterns = [
    path('procurements/', ProcurementsAPIView.as_view(), name='procurements'),
]