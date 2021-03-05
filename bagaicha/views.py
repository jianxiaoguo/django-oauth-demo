import base64
import hashlib
import urllib
import uuid
import json

import requests
from authlib.integrations.django_client import OAuth
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import include, path
from django.views.generic.base import TemplateView

from gatepass.oauth.client import OAUTH_CLIENT_ID, OAUTH_ACCESS_TOKEN_URL, OAUTH_AUTHORIZE_URL, OAUTH_CLIENT_SECRET, OAUTH_REFRESH_TOKEN_URL
from gatepass.oauth.client import GatepassOAuthClient

# Create your views here.

gp_client =GatepassOAuthClient(
    client_id=OAUTH_CLIENT_ID,
    client_secret=OAUTH_CLIENT_SECRET
)

gp_client.configure(
    authorize_url=OAUTH_AUTHORIZE_URL,
    access_token_url=OAUTH_ACCESS_TOKEN_URL,
    refresh_token_url=OAUTH_REFRESH_TOKEN_URL,
    code_challenge=True,
    code_challenge_method='S256'
)

class LoginWithView(TemplateView):
    template_name='demo.html'

    def get_context_data(self, **kwargs):
        kw=super().get_context_data(**kwargs)

        redirect_url = 'http://g.uucin.com/login/generic_oauth'
        authorize_url = gp_client.generate_authorize_url(redirect_url)

        self.request.session['code_challenge'] = authorize_url.get('code_challenge')
        self.request.session['state'] = authorize_url.get('state')

        kw['authorize_url'] = authorize_url['url']
        print(kw['authorize_url'])
        kw['args'] = urllib.parse.urlparse(authorize_url['url']).query.split("&")
        kw['state'] = authorize_url['state']

        return kw

class RedirectUrlView(TemplateView):
    template_name='redirect.html'

    def get_context_data(self, **kwargs):
        kw = super().get_context_data(**kwargs)
        kw['get_args'] = self.request.GET

        # make access_Token_request
        # client=oauth_client()
        resp1={'code': self.request.GET.get('code'), 'state': self.request.GET.get('state')}

        code=self.request.GET.get('code')
        state=self.request.GET.get('state')

        code_challenge=self.request.session.get('code_challenge')

        redirect_url = self.request.build_absolute_uri('/login/generic_oauth')
        _response = gp_client.make_access_token_request(code=code, state=state, redirect_uri=redirect_url, code_challenge=code_challenge)

        response = json.loads(_response.text)
        kw['response'] = response

        kw['refresh_token'] = response.get('refresh_token')
        return kw

class RefreshTokenView(TemplateView):
    template_name='refresh.html'

    def get_context_data(self, **kwargs):
        kw = super().get_context_data(**kwargs)
        kw['get_args'] = self.request.GET

        # make access_Token_request
        # client=oauth_client()

        refresh_token=self.request.GET.get('token')

        redirect_url = self.request.build_absolute_uri('/login/generic_oauth')
        _response = gp_client.make_refresh_token_request(refresh_token)

        response = json.loads(_response.text)

        kw['response'] = response
        return kw