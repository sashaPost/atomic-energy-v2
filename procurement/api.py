from rest_framework import generics
from .models import Procurement
from .serializers import ProcurementSerializer
from news.permissions import IsAuthenticatedReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication



@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementsList(generics.ListAPIView):
    queryset = Procurement.objects.filter(visibility=True)
    serializer_class = ProcurementSerializer

@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])    
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementDetail(generics.RetrieveAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
