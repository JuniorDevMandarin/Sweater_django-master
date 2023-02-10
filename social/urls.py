from django.urls import path, re_path
from django.views.decorators.cache import cache_page


from . import views
from .views import *


urlpatterns = [
    path('', SocialHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name="delete_post"),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', SocialCategory.as_view(), name='category'),
    path('like/', like, name='like'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='social/change_password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='social/change_password.html')),
    path('password_success', views.password_success, name="password_success"),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]