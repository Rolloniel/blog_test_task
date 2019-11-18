"""base_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('news/', include('news.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views
from django.contrib.auth.decorators import login_required


from base_ui import views as base_ui_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', allauth_views.SignupView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='auth_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('', base_ui_views.ShowHomeView.as_view()),
    path('news/', base_ui_views.NewsListView.as_view(), name='news_list'),
    path('news/premoderation/', base_ui_views.NewsPremoderationListView.as_view(), name='news_premoderation'),
    path('news/add_news/', login_required(base_ui_views.NewsAddView.as_view()), name='news_add'),
    re_path(r'^news/(?P<pk>\d+)/?$', base_ui_views.NewsDetailView.as_view(), name='news_detail'),
    re_path(r'^news/(?P<pk>\d+)/edit/?$', base_ui_views.NewsEditView.as_view(), name='news_edit'),
    path('comments/', include('django_comments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
