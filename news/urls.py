from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from .api import *
from .views import *



urlpatterns = [
    path('root/', api_root),  
]
urlpatterns += [
     path('users/', 
          UserList.as_view(), 
          name='user-list'),
     path('users/<int:pk>/', 
          UserDetail.as_view(), 
          name='user-detail'),
]
urlpatterns += [    
     path('category/', 
          CategoryList.as_view(),
          name='category-list'), 
     path('category/<int:pk>/',
          CategoryDetail.as_view(),
          name='category-detail'),
     path('category/<int:pk>/en-posts/',
          CategoryEnPostsList.as_view(),
          name='category-en-posts-list'),
]
urlpatterns += [
     path('posts/', 
          PostList.as_view(), 
          name='post-list'),
     path('en-posts/',
          EnPostsList.as_view(),
          name='test'
          ),
     path('posts/<int:pk>/', 
          PostDetail.as_view(), 
          name='post-detail'),
     path('posts/<int:pk>/ua-post-head-detail/',
          UaPostHeadDetail.as_view(),
          name='uaposthead-detail'),
     path('posts/<int:post_pk>/ua-post-body-detail/<int:ua_post_body_pk>/',
          UaPostBodyDetail.as_view(),
          name='uapostbody-detail'),
     path('posts/<int:post_pk>/ua-post-body-list/',
          UaPostBodyList.as_view(),
          name='uapostbody-list'),
     path('posts/<int:pk>/en-post-head-detail/',
          EnPostHeadDetail.as_view(),
          name='enposthead-detail'),
     path('posts/<int:pk>/en-post-body-detail/<int:en_post_body_pk>/', 
          EnPostBodyDetail.as_view(),
          name='enpostbody-detail'),
     path('posts/<int:post_pk>/en-post-body-list/',
          EnPostBodyList.as_view(),
          name='enpostbody-list'),
]
urlpatterns += [
    path('posts/<int:post_pk>/post-attachments/<int:pk>/',
         PostAttachmentsDetail.as_view(),
         name='postattachments-detail'),
]
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]
urlpatterns += staticfiles_urlpatterns()
urlpatterns = format_suffix_patterns(urlpatterns)
