"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('Blog/', include('Blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from . import views
from captcha import views as ca_view

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('Blog.urls')),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('comment/', include('comment.urls')),
    path('likes/', include('likes.urls')),
    path('captcha/', include('captcha.urls')),

    path('refresh/', ca_view.captcha_refresh, name='captcha-refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_for_modal/', views.login_for_medal, name='login_for_medal'),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('chenge_nickname/', views.change_nickname, name='chenge_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_email/', views.send_email_code, name='send_email'),
    path('change_pwd/', views.rechange_pwd, name='change_pwd'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),


]
urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
