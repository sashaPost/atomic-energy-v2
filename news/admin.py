from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import *
from django.template.loader import get_template
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.


# admin.site.register(Category)
class PostInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if not any(post_form.cleaned_data.get('title_ua') or post_form.cleaned_data.get('title_eng') for post_form in self.forms):
            raise ValidationError('At least one Post should have a non-empty title_ua or title_eng.')

class PostInline(admin.TabularInline):
    formset = PostInlineFormSet
    model = Post
    extra = 0
    show_change_links = True
    # fields = ('meta_title', 'meta_description', 'post_visibility', 'pub_date', 'added_by')
    # readonly_fields = ('pub_date', 'added_by')
    # ordering = ('-pub_date',)
    fields = ('id', 'display_title_ua', 'display_title_en', 'indicated_date', 'post_link')
    readonly_fields = ('id', 'display_title_ua', 'display_title_en', 'indicated_date', 'post_link')
    show_change_links = True
    
    # def has_add_permission(self, request, obj):
    #     return True
    def display_title_ua(self, obj):
        ua_head = obj.ua_head.first()
        return ua_head.title_ua if ua_head else ''
    
    display_title_ua.short_description = 'Title (UA)'
    
    def display_title_en(self, obj):
        en_head = obj.en_head.first()
        return en_head.title_eng if en_head else ''
    
    display_title_en.short_description = 'Title (EN)'  
    
    def post_link(self, obj):
        edit_url = reverse('admin:news_post_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', edit_url, 'Edit')
    
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('ua_cat', 'en_cat')
    search_fields = ('ua_cat', 'en_cat')
    inlines = [PostInline]
    # list_per_page = 10
    
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #     queryset |= self.model.objects.filter(post__meta_title__incontains=search_term)
    #     return queryset, use_distinct
    
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     category = Category.objects.get(pk=object_id)
    #     posts = category.post.all().order_by('-pub_date')
    #     paginator = Paginator(posts, 50)
    #     page = request.GET.get('page', 1)
        
    #     try:
    #         current_page = paginator.page(page)
    #     except (EmptyPage, InvalidPage):
    #         current_page = paginator.page(paginator.num_pages)
            
    #     extra_context['posts'] = current_page
    #     extra_context['category'] = category
    #     return super().change_view(request, object_id, form_url, extra_context=extra_context)
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields # Make category fields readonly
    #     return self.readonly_fields
    
    def has_add_permission(self, request):
         return True
     
    def has_delete_permission(self, request, obj=None):
        return True
    
# admin.site.register(Category, CategoryModelAdmin)

class UaPostHeadInline(admin.StackedInline):
    model = UaPostHead
    max_num = 1
    extra = 1
    readonly_fields = ('id',)
    fk_name = 'post'
    show_change_link = True
    prepopulated_fields = {"slug": ("title_ua",)}

    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
class UaPostBodyInline(admin.StackedInline):
    model = UaPostBody
    extra = 1
    readonly_fields = ('id',)
    fk_name = 'post'
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
class EnPostHeadInline(admin.StackedInline):
    model = EnPostHead
    max_num = 1
    extra = 0 
    readonly_fields = ('id',)
    fk_name = 'post'
    show_change_link = True
    prepopulated_fields = {"slug": ("title_eng",)}
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
class EnPostBodyInline(admin.StackedInline):
    model = EnPostBody
    extra = 0
    readonly_fields = ('id',)
    fk_name = 'post'
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

class PostAttachmentsInline(admin.StackedInline):
    model = PostAttachments
    extra = 0
    readonly_fields = ('id',)
    fk_name = 'post'
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    # inlines = (PostImagesInline, UaPostMessageInline, EnPostMessageInline, PostAttachmentsInline)   # add appropriate classes for 'PostAttachments', 'UaPostMessage', 'EnPostMessage'
    inlines = (UaPostHeadInline, UaPostBodyInline, EnPostHeadInline, EnPostBodyInline, PostAttachmentsInline)
    fields = (
        'meta_title',
        'meta_description',
        'seo_tags',
        'post_visibility',
        'preview_image',
        'image_alt',
        'image_visibility',
        'indicated_date',
        'added_by',
        'category',
        
        # 'title_ua',
        # 'title_eng',
        # 'slug',
        # 'category',
        # 'preview_text_ua',
        # 'preview_text_eng',
        # 'meta_title',
        # 'preview_image',
        # # 'visibility_image',
        # 'image_alt',
        # 'message_ua',
        # 'message_eng',
        # # 'visibility',
        # 'meta_description',
        # # 'pub_date',   # shouldn't be specified here; delete later
        # 'indicated_date',
        # 'seo_tags',
        # 'added_by',
    )
    # prepopulated_fields = {"slug": ("title_ua",)}
    
    def image_inline(self, obj=None, *args, **kwargs):
        context = obj.response['context_data']
        inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(0)
        return get_template(inline.opts.template).render(context, self.request)

    def render_change_form(self, request, context, *args, **kwargs):
        instance = context['adminform'].form.instance   # get the model instance from modelform
        instance.request = request
        instance.response = super().render_change_form(request, context, *args, **kwargs)
        return instance.response
    
    list_display = ('id', 'title_ua', 'title_en', 'category_name', 'indicated_date')
    
    def title_ua(self, obj):
        ua_head = obj.ua_head.first()
        return ua_head.title_ua if ua_head else ''
    
    title_ua.short_description = 'Title (UA)'
    
    def title_en(self, obj):
        en_head = obj.en_head.first()
        return en_head.title_eng if en_head else ''
    
    title_en.short_description = 'Title (EN)'
    
    def category_name(self, obj):
        return obj.category.ua_cat if obj.category else ''
    
    category_name.short_description = 'Category'
    category_name.admin_order_field = 'category__ua_cat'
        
    
        
    # debugging shit
    # import pdb; pdb.set_trace()

# @admin.register(PostImages)
# class PostImagesModelAdmin(admin.ModelAdmin):
#     fields = (
#             'post',
#             'image',
#             'image_alt',
#         )
    