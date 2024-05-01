from .api import ProcurementsList, ProcurementDetail, ProcurementListByYear, ProcurementListByUnit
from django.urls import include, path
# from .api import ProcurementViewSet
# from rest_framework.routers import DefaultRouter



# router = DefaultRouter()

# router.register('procurements', ProcurementViewSet, basename='procurement')

urlpatterns = [
    path('procurements/', ProcurementsList.as_view(), name='procurements'),
    path('procurements/<int:pk>/', ProcurementDetail.as_view(), name='procurement-detail'),
    path('procurements/year', ProcurementListByYear.as_view()),    # + ?search=2022
    path('procurements/unit', ProcurementListByUnit.as_view()),    # + ?search=HNPP / ?search=ХАЕС
    
    # path('', include(router.urls)),
]

