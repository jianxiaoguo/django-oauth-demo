app_name = 'bagaicha'

import base64
import hashlib
import urllib
import uuid

import requests
from authlib.integrations.django_client import OAuth
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic.base import TemplateView

from .views import LoginWithView, RedirectUrlView

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='bagaicha.html'))),
    path('demo/', LoginWithView.as_view(), name='demo'),
    path('private/', RedirectUrlView.as_view(), name='private')
]


# def generate_code_challenge():
#     #randomkey = str(uuid.uuid4())
#     randomkey = str("PredictableDemoCode")
#     return hashlib.sha256(randomkey.encode()).hexdigest()

# def oauth_client():
#     oauth=OAuth()
#     try:
#         oauth.register(
#             name='bagaicha',
#             client_id='2H7EwXHRy5YESvL8AkBVJtzGQVOgo3geu3DaWfWf',
#             client_secret='vQ8KAITx0HFu3CI496iQdAs8NzhvIdz94aWTkmBYVR77h52qiiLzsZrhH5nVE5BPd67vkYuptDRJk5W83tsjFekXrTCy908zdqCXbgLT7pRxPsT4l2QTX52YMISFbkvR',
#             access_token_url='http://dev.khalti.com.np:8004/o/token/',
#             access_token_params=None,
#             refresh_token_url=None,
#             authorize_url='http://dev.khalti.com.np:8004/o/authorize/',
#             client_kwargs=dict(code_challenge=generate_code_challenge(), code_challenge_method='S256', client_user_identifier='uid:109adfadsa'),
#         )
#     except Exception as exc:
#         raise

#     return oauth.bagaicha
