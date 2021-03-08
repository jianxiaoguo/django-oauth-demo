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
from django.http import HttpResponse
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, View
from django.contrib.auth.decorators import login_required

import oauth2_provider.views as oauth2_views

urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('token', oauth2_views.TokenView.as_view(), name="token"),
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


from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

class UserList(View):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        import json
        token_value = request.headers['Authorization'][7:]  # Bearer ****
        # token_value = request.META.get("HTTP_AUTHORIZATION")[7:]  # tong shang
        from oauth2_provider.models import get_access_token_model
        token = (
            get_access_token_model().objects.select_related("user", "application").get(token=token_value)
        )
        print(token)
        return HttpResponse(json.dumps({"name":token.user.username, "email":token.user.email}))

class UserDetails(View):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        import json
        return HttpResponse(json.dumps({"name":"test", "email":"test@test"}))

class GroupList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

urlpatterns += [
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('users/emails', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]
