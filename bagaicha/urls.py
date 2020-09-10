app_name = 'bagaicha'

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from authlib.integrations.django_client import OAuth

import hashlib
import uuid

import urllib

def generate_challenge_code():
    #randomkey = str(uuid.uuid4())
    randomkey = str("PredictableDemoCode")
    return hashlib.sha256(randomkey.encode()).hexdigest()

def oauth_client():
    oauth=OAuth()
    try:
        oauth.register(
            name='bagaicha',
            client_id='2H7EwXHRy5YESvL8AkBVJtzGQVOgo3geu3DaWfWf',
            client_secret='vQ8KAITx0HFu3CI496iQdAs8NzhvIdz94aWTkmBYVR77h52qiiLzsZrhH5nVE5BPd67vkYuptDRJk5W83tsjFekXrTCy908zdqCXbgLT7pRxPsT4l2QTX52YMISFbkvR',
            access_token_url='http://dev.khalti.com.np:8004/o/token/',
            access_token_params=None,
            refresh_token_url=None,
            authorize_url='http://dev.khalti.com.np:8004/o/authorize/',
            client_kwargs=dict(challenge_code=generate_challenge_code(), challenge_code_method='s256', client_user_identifier='uid:109adfadsa'),
        )
    except Exception as exc:
        raise

    return oauth.bagaicha


class LoginWithView(TemplateView):
    template_name='demo.html'

    def get_context_data(self, **kwargs):
        kw=super().get_context_data(**kwargs)

        client=oauth_client()

        redirect_url = self.request.build_absolute_uri('/bagaicha/private/')
        authorize_url = client.create_authorization_url(redirect_url,**client.client_kwargs)

        kw['authorize_url'] = authorize_url['url']
        kw['args'] = urllib.parse.urlparse(authorize_url['url']).query.split("&")
        kw['state'] = authorize_url['state']
        return kw

class RedirectUrlView(TemplateView):
    template_name='redirect.html'

    def get_context_data(self, **kwargs):
        kw = super().get_context_data(**kwargs)
        kw['get_args'] = self.request.GET

        # make access_Token_request
        client=oauth_client()
        resp1={'code': self.request.GET.get('code'), 'state': self.request.GET.get('state')}
        import pdb
        pdb.set_trace()
        response = client.authorize_access_token(self.request)
        kw['response'] = response
        return kw


urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='bagaicha.html'))),
    path('demo/', LoginWithView.as_view()),
    path('private/', RedirectUrlView.as_view())
]

