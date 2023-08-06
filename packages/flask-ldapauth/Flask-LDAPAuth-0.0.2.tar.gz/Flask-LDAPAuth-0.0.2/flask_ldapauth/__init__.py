import ldap
import jwt

from datetime import datetime, timedelta
from flask import Flask, current_app, _app_ctx_stack, request, jsonify

from typing import Dict, List

user_attributes = [
    'mail',
    'cn',
    'uid',
    'givenname',
    'sn'
]

group_attributes = [
    'memberuid'
]


class Protector(object):

    def __init__(self, data: bool = False, key: str = ""):
        self.data = data
        self.key = key

    def __call__(self, func):

        def wrapper(*args, **kvargs):

            json, cookies = request.json, request.cookies

            auth_header = request.headers.get("token", False)
            auth_cookie = cookies.get('token', False)

            if auth_header is False and auth_cookie is False:
                return jsonify({'mesg': 'Missing token'}), 401

            token = JWTToken(key=self.key)

            if auth_header:
                if token.validate(token=auth_header) is False:
                    return jsonify({'mesg': 'Invalid token'}), 401
            else:
                if token.validate(token=auth_cookie) is False:
                    return jsonify({'mesg': 'Invalid token'}), 401

            if self.data:
                return func(json, *args, **kvargs)

            return func(*args, **kvargs)

        return wrapper


class JWTToken(object):

    def __init__(self, key: str = "", expire: int = 0):
        self.expire = expire
        self.key = key

    def validate(self, token: str):

        try:
            jwt.decode(token, self.key, algorithms='HS256')
        except Exception as e:
            return False

        return True

    def create(self, payload: Dict = {}):

        if self.key is None:
            return

        payload['exp'] = datetime.now() + timedelta(days=self.expire)

        return jwt.encode(payload, self.key)

    def protected(self):

        return Protector()


class LDAPAuth(object):

    def __init__(self, app: Flask = None):
        self.ldap_url = app.config.get('LDAP_URL', None)
        self.root_dn = app.config.get('LDAP_ROOTDN', None)
        self.users_dn = app.config.get('LDAP_USERDN', True)
        self.group = app.config.get('LDAP_GROUP', False)
        self.start_tls = app.config.get('LDAP_START_TLS', True)
        self.user_filter = app.config.get('LDAP_USER_FILTER', 'cn')
        self.timeout = app.config.get('LDAP_TIMEOUT', 10)
        self.secret_key = app.config.get('SECRET_KEY', None)
        self.expire = app.config.get('LDAP_TOKEN_EXPIRE', 8)

        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: Flask):
        app.teardown_appcontext(self.teardown)

    def connect(self,
                return_user: bool = False,
                keep_alive: bool = False,
                username: str = "",
                password: str = "",
                user_attributes: List = user_attributes):

        user_info = {}

        userdn = f"cn={username},{self.users_dn}"

        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, self.timeout)

        self.conx = ldap.initialize(self.ldap_url)

        if self.start_tls:
            try:
                self.conx.start_tls_s()
            except Exception as e:
                return False

        try:
            self.conx.simple_bind_s(userdn, password)
        except Exception as e:
            self.disconnect()
            return False

        if self.group:

            members = self.groups()

            if username not in members:
                self.disconnect()
                return False

        if return_user is True:
            user_info = self.user(
                username=username, attributes=user_attributes)

        if keep_alive is False:
            self.disconnect()
        else:
            ctx = _app_ctx_stack.top

            if ctx is not None:
                if not hasattr(ctx, 'ldap_auth'):
                    ctx.ldap_auth = self.conx

        return user_info

    def teardown(self, exception):
        ctx = _app_ctx_stack.top

        if hasattr(ctx, 'ldap_auth'):
            ctx.ldap_auth.unbind_s()

    def disconnect(self):

        self.conx.unbind_s()

    def user(self,
             username: str = "",
             attributes: List = user_attributes):

        search_filter = f"(&(objectClass=person)({self.user_filter}={username}))"

        search = self.conx.search_s(
            self.root_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)

        dn, data = search.pop()

        decode_data = {}

        for k, i in data.items():
            decode_data[k] = " ".join([x.decode() for x in i])

        return decode_data

    def groups(self):

        members = []

        search_filter = f"(&(objectClass=posixGroup)(cn={self.group}))"

        search = self.conx.search_s(
            self.root_dn, ldap.SCOPE_SUBTREE, search_filter, group_attributes)

        if not search:
            return members

        dn, data = search.pop()

        for i in data['memberUid']:
            members.append(i.decode())

        return members

    @property
    def token(self):

        return JWTToken(key=self.secret_key, expire=self.expire)

    def protected(self, data: bool = False):
        return Protector(data=data, key=self.secret_key)
