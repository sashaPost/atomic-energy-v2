import pdb
from django.contrib.auth.models import User
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from .models import (
    Category, 
    Post,
    UaPostHead,
    UaPostBody,
    EnPostHead,
    EnPostBody,
    PostAttachments,
) 
from .permissions import IsAuthenticatedReadOnly

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, Paginator
from rest_framework import permissions, serializers, status
from rest_framework.reverse import reverse

from django.db.models import F




class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail',
                                               lookup_field='pk',)
    posts = serializers.HyperlinkedRelatedField(many=True, 
                                                read_only=True,
                                                view_name='post-detail', 
                                                lookup_field='pk',)

    class Meta:
        model = User
        fields = '__all__'
        
class UaPostHeadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='uaposthead-detail',
                                               lookup_field='pk',)
    post = serializers.HyperlinkedRelatedField(many=False,
                                               read_only=True,
                                               view_name='post-detail',
                                               lookup_field='pk',)
    class Meta:
        model = UaPostHead
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super(UaPostHeadSerializer, self).to_representation(instance)
        if data['preview_text_ua'] in ['', None, 0]:
            data['preview_text_ua'] = False
        return data

class UaPostBodySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    post = serializers.HyperlinkedRelatedField(many=False,
                                               read_only=True,
                                               view_name='post-detail',
                                               lookup_field='pk',)
    class Meta:
        model = UaPostBody
        fields = '__all__'
        
    def get_url(self, obj):
        post = obj.post
        request = self.context.get('request')
        return reverse('uapostbody-detail', args=[str(post.pk), str(obj.pk)], request=request, format=None)
    
    def to_representation(self, instance):
        data = super(UaPostBodySerializer, self).to_representation(instance)

        if data['image'] in [None, '', 'https://tested.energoatom.com.ua/media/False']:
            data['image'] = False
        if data['video_url'] in ['false', 'False', 'No Video', None]:
            data['video_url'] = False

        # new code:
        if data['image']:
            data['image'] = data['image'].replace('tested', 'new')

        return data
        
class EnPostHeadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='enposthead-detail',
                                               lookup_field='pk',)
    post = serializers.HyperlinkedRelatedField(many=False,
                                               read_only=True,
                                               view_name='post-detail',
                                               lookup_field='pk',)
    class Meta:
        model = EnPostHead
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super(EnPostHeadSerializer, self).to_representation(instance)
        if data['preview_text_en'] in ['', None]:
            data['preview_text_en'] = False
        return data

class EnPostBodySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    post = serializers.HyperlinkedRelatedField(many=False,
                                               read_only=True,
                                               view_name='post-detail',
                                               lookup_field='pk',)
    class Meta:
        model = EnPostBody
        fields = '__all__'
        
    def get_url(self, obj):
        post = obj.post
        request = self.context.get('request')
        return reverse('enpostbody-detail', args=[str(post.pk), str(obj.pk)], request=request, format=None)
    
    def to_representation(self, instance):
        data = super(EnPostBodySerializer, self).to_representation(instance)

        if data['image'] in [None, '', 'https://tested.energoatom.com.ua/media/False']:
            data['image'] = False
        if data['video_url'] in ['false', 'False', 'No Video', None]:
            data['video_url'] = False

        if data['image']:
            data['image'] = data['image'].replace('tested', 'new')

        return data

class EnPostsSerializer(serializers.ModelSerializer):
    en_head = EnPostHeadSerializer(many=True, read_only=True)
    en_body = EnPostBodySerializer(many=True, read_only=True)
    
    category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        
    def get_category(self, obj):
        try:
            request = self.context['request']
            category_url = reverse('category-detail', args=[obj.category.pk], request=request)
            return {
                'id': obj.category.pk,
                'url': category_url,
                'ua_cat': obj.category.ua_cat,
                'en_cat': obj.category.en_cat,
            }
        except AttributeError as e:
            return False
    
    

class PostAttachmentsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    post = serializers.HyperlinkedRelatedField(many=False,
                                               read_only=True,
                                               view_name='post-detail',
                                               lookup_field='pk',)
    class Meta:
        model = PostAttachments
        fields = '__all__'
        
    def get_url(self, obj):
        post = obj.post
        request = self.context.get('request')
        return reverse('postattachments-detail', args=[str(post.pk), str(obj.pk)], request=request, format=None)

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post-detail',
                                               lookup_field='pk',)
    ua_head = UaPostHeadSerializer(many=True, read_only=True, )    # source='ua_head'
    ua_body = UaPostBodySerializer(many=True, read_only=True)
    en_head = EnPostHeadSerializer(many=True, read_only=True)
    en_body = EnPostBodySerializer(many=True, read_only=True)
    attachments = PostAttachmentsSerializer(many=True, read_only=True)
    
    category = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
        
    def get_category(self, obj):
        try:
            request = self.context['request']
            category_url = reverse('category-detail', args=[obj.category.pk], request=request)
            return {
                'id': obj.category.pk,
                'url': category_url,
                'ua_cat': obj.category.ua_cat,
                'en_cat': obj.category.en_cat,
            }
        except AttributeError as e:
            return False
    
    # commented with latest update:
    # def to_representation(self, instance):
    #     data = super(PostSerializer, self).to_representation(instance)

    #     if data['preview_image'] in [None, '', 'https://tested.energoatom.com.ua/media/False']:
    #         data['preview_image'] = False

    #     if data['preview_image']:
    #         data['preview_image'] = data['preview_image'].replace('tested', 'new')

    #     return data
        
class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail',
                                               lookup_field='pk',)
    posts = serializers.SerializerMethodField()
        
    class Meta:
        model = Category
        fields = '__all__'
        
    def get_posts(self, obj):
        request = self.context['request']
        # user = request.user
        
        # works:
        posts = Post.objects.filter(category=obj).order_by('-pub_date')

        # # test:
        posts_test = Post.objects.filter(category=obj)
        posts_test_upd = posts.order_by(F('migrated_novelty').asc(), '-old_date', '-indicated_date')
        # print('posts_test_upd: ', posts_test_upd)
        # posts = posts.order_by('-migrated_novelty', '-old_date', 'visible_date')
        # print("All Posts Pub Dates:", [post for post in posts_test_upd])

        # Debugging statements
        # print("All Posts Pub Dates:", [post.pub_date for post in posts])

        page_size = 12
        # paginator = Paginator(posts, page_size)
        paginator = Paginator(posts_test_upd, page_size)
        
        page_number = request.query_params.get('page', 1)
        try:
            current_page = paginator.page(page_number)
            context = {'request': request}
            serializer = PostSerializer(current_page, many=True, context=context)            
            return serializer.data
        except EmptyPage:
            error_message = {"error": "Page does not exist"}
            return error_message, status.HTTP_404_NOT_FOUND
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_posts'] = instance.post.count()
        return representation        
    
class CategoryEnPostsSerializer(serializers.ModelSerializer):
    en_head = EnPostHeadSerializer(many=True, read_only=True)
    en_body = EnPostBodySerializer(many=True, read_only=True)
    
    category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        
    def get_category(self, obj):
        try:
            request = self.context['request']
            category_url = reverse('category-detail', args=[obj.category.pk], request=request)
            return {
                'id': obj.category.pk,
                'url': category_url,
                'ua_cat': obj.category.ua_cat,
                'en_cat': obj.category.en_cat,
            }
        except AttributeError as e:
            return False
    