"""kklogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

import oauth2_provider.views as oauth2_views

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pass_reset/', auth_views.LoginView.as_view(), name='password_reset'),
]

urlpatterns += [
    path('bagaicha/', include('bagaicha.urls', namespace='bagaicha')),
        ]

urlpatterns += [
        path('',  RedirectView.as_view(url='bagaicha/'))
        ]

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

    # OAuth2 Application Management endpoints
oauth2_endpoint_views += [
    path('applications/', login_required(oauth2_views.ApplicationList.as_view()), name="list"),
    path('applications/register/', login_required(oauth2_views.ApplicationRegistration.as_view()), name="register"),
    path('applications/<pk>/', login_required(oauth2_views.ApplicationDetail.as_view()), name="detail"),
    path('applications/<pk>/delete/', login_required(oauth2_views.ApplicationDelete.as_view()), name="delete"),
    path('applications/<pk>/update/', login_required(oauth2_views.ApplicationUpdate.as_view()), name="update"),
]

# OAuth2 Token Management endpoints
oauth2_endpoint_views += [
    path('authorized-tokens/', login_required(oauth2_views.AuthorizedTokensListView.as_view()), name="authorized-token-list"),
    path('authorized-tokens/<pk>/delete/', login_required(oauth2_views.AuthorizedTokenDeleteView.as_view()),
        name="authorized-token-delete"),
]

urlpatterns += [
    # OAuth 2 endpoints:
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
]

