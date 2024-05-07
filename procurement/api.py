from .models import Procurement
from .serializers import ProcurementSerializer
from news.permissions import IsAuthenticatedReadOnly
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import ExtractYear
from rest_framework.pagination import PageNumberPagination
import logging


logger = logging.getLogger(__name__)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6  # You can adjust the default page size here
    # page_size_query_param = 'page_size'
    # max_page_size = 6
    

@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class ProcurementsList(generics.ListAPIView):
    queryset = Procurement.objects.filter(visibility=True)\
        .annotate(year=ExtractYear('date'))
    serializer_class = ProcurementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['date__year', 'unit__id', 'tender_id']  # Combine search fields
    ordering_fields = ['date', 'value__amount'] 
    ordering = '-date' 
    pagination_class = LargeResultsSetPagination
    
    def get_paginated_response(self, data):
        years_list = set(item['date'][:4] for item in data)
        response = super().get_paginated_response(data)
        response.data['years'] = list(years_list)
        return response
    
    
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
    
    
@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
class ProcurementSearch(APIView):
    """API endpoint to retrieve a single Procurement record by tender_id.
    """
    def get(self, request, tender_id):
        try:
            procurement = Procurement.objects.get(tender_id=tender_id)
            serializer = ProcurementSerializer(procurement, context={'request': request})
            return Response(serializer.data)
        except Procurement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # def get(self, request):
    #     query_string = request.query_params.get('q')
    #     if query_string:
    #         results = search_procurements(query_string)
    #         return Response(results)
    #     return Response({
    #         'message': 'Missing query search parameter.'
    #     })
