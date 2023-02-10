from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class SocialAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Social
        fields = '__all__'


class SocialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',  'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    form = SocialAdminForm
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        'title', 'slug', 'cat', 'author', 'content', 'photo', 'is_published', 'get_html_photo', 'time_create', 'time_update', 'likes')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Social, SocialAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
admin.site.register(Comment)