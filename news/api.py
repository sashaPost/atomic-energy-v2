"""
docstring placeholder.
"""
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import (generics, 
                            permissions, 
                            renderers, 
                            status, 
                            viewsets)
from rest_framework.authentication import (
    SessionAuthentication, 
    BasicAuthentication,
)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import *
from .serializers import (
    PostSerializer, 
    UserSerializer,
    UaPostHeadSerializer,
    UaPostBodySerializer,
    EnPostHeadSerializer,
    EnPostBodySerializer,
    PostAttachmentsSerializer,
    CategorySerializer,
    EnPostsSerializer,
    CategoryEnPostsSerializer,
)
from .permissions import IsAuthenticatedReadOnly
import pdb
from rest_framework_simplejwt.authentication import JWTAuthentication



@api_view(['GET'])
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
def api_root(request, format=None):    # OR format='json' 
    """
    # test
    Docstring message is being rendered on the API route.
    """
    return Response({
            'users': reverse('user-list', request=request, format=format),
            'categories': reverse('category-list', request=request, format=format),
            'posts': reverse('post-list', request=request, format=format),
        })
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class UserList(generics.ListAPIView):
    """
    List of registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedReadOnly]

@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedReadOnly]
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedReadOnly]
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class UaPostHeadDetail(generics.RetrieveAPIView):
    queryset = UaPostHead.objects.all()
    serializer_class = UaPostHeadSerializer
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class UaPostBodyDetail(generics.RetrieveAPIView):
    queryset = UaPostBody.objects.all()
    serializer_class = UaPostBodySerializer
    lookup_url_kwarg = 'ua_post_body_pk'
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class UaPostBodyList(generics.ListAPIView):
    queryset = UaPostBody.objects.all()
    serializer_class = UaPostBodySerializer
    
    def get_queryset(self):
        # pdb.set_trace()
        post_pk = self.kwargs.get('post_pk')
        queryset = UaPostBody.objects.filter(post=post_pk)
        return queryset
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class EnPostHeadDetail(generics.RetrieveAPIView):
    queryset = EnPostHead.objects.all()
    serializer_class = EnPostHeadSerializer
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class EnPostBodyDetail(generics.RetrieveAPIView):
    queryset = EnPostBody.objects.all()
    serializer_class = EnPostBodySerializer
    lookup_url_kwarg = 'en_post_body_pk'
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class EnPostBodyList(generics.ListAPIView):
    queryset = EnPostBody.objects.all()
    serializer_class = EnPostBodySerializer
    
    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        queryset = EnPostBody.objects.filter(post=post_pk)
        return queryset
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class PostAttachmentsDetail(generics.RetrieveAPIView):
    queryset = PostAttachments.objects.all()
    serializer_class = PostAttachmentsSerializer
    # lookup_url_kwarg = 'pk'
        
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class PostList(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-indicated_date')
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedReadOnly]
    
@authentication_classes([
    # BasicAuthentication,
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class EnPostsList(generics.ListAPIView):
    serializer_class = EnPostsSerializer
    
    def get_queryset(self):
        return Post.objects.filter(en_head__isnull=False, en_body__isnull=False).distinct()
    
    def get_serializer_context(self):
        return {'request': self.request}

@authentication_classes([
    SessionAuthentication, 
    JWTAuthentication,
])
@permission_classes([IsAuthenticatedReadOnly])
class CategoryEnPostsList(generics.ListAPIView):
    serializer_class = CategoryEnPostsSerializer
    
    def get_queryset(self):
        print(self.kwargs)
        category_id = self.kwargs.get('pk')
        queryset = Post.objects.filter(category=category_id, en_head__isnull=False, en_body__isnull=False).distinct()
        return queryset