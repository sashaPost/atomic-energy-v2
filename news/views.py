"""
docstring placeholder.
"""
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .serializers import (PostSerializer, 
                          UserSerializer)
from .permissions import IsAuthenticatedReadOnly



def test(request):
    post = Post.objects.get(id=5)
    context = {
        'post': post.message_ua,
    }
    return render(request=request, template_name='news/test.html', context=context)


