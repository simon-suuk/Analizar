import json
import os

import requests
from flask import url_for, request, redirect, session
from rauth import OAuth1Service, OAuth2Service


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = json.loads(os.environ.get("OAUTH_CREDENTIALS"))[provider_name]
        # credentials = os.environ["OAUTH_CREDENTIALS"][provider_name]
        # credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        # print('typeofdata: {}, credentials: {}'.format(type(credentials), credentials))
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email,manage_pages,read_insights',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()
                  },
            decoder=decode_json
        )

        account_data = self.exchange_access_token_for_page_tokens(oauth_session.access_token)

        me = oauth_session.get('me?fields=id,email').json()
        # print('My access token key is: {}'.format(oauth_session.access_token))
        # Facebook does not provide username, so the email's user is used instead
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email'),
            account_data
        )

    def exchange_access_token_for_page_tokens(self, short_term_token):
        token_base_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token"
        token_url = "{token_base_url}&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={fb_exchange_token}".format(
            token_base_url=token_base_url,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            fb_exchange_token=short_term_token
        )
        long_term_token = requests.get(token_url).json()['access_token']

        pages_base_url = "https://graph.facebook.com"
        version = "v2.12"
        pages_url = "{pages_base_url}/me?fields=accounts&access_token={access_token}".format(
            pages_base_url=pages_base_url,
            version=version,
            access_token=long_term_token
        )

        return requests.get(pages_url).json()['accounts']['data']


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None  # Twitter does not provide email
