from rest_framework import generics
from .models import Procurement
from .serializers import ProcurementSerializer



class ProcurementsAPIView(generics.ListAPIView):
    queryset = Procurement.objects.order_by('date')
    serializer_class = ProcurementSerializer
