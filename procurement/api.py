from .models import Procurement
from .serializers import ProcurementSerializer
from news.permissions import IsAuthenticatedReadOnly
from rest_framework import generics
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementsList(generics.ListAPIView):
    queryset = Procurement.objects.filter(visibility=True)
    serializer_class = ProcurementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['date__year', 'unit__id']  # Combine search fields
    ordering_fields = ['date', 'value__amount'] 
    ordering = '-date' 

@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])    
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementDetail(generics.RetrieveAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer


@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])    
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementListByYear(generics.ListAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date__year']


@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])    
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementListByUnit(generics.ListAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
    filter_backends = [filters.SearchFilter]
    # search_fields = ['unit__ua_name', 'unit__en_name']
    search_fields = ['unit__id']
