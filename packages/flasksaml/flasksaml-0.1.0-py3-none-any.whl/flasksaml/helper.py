import os
from urllib.parse import urlparse

from flask import request
from onelogin.saml2.auth import OneLogin_Saml2_Auth

SAML_SETTINGS_PATH = os.environ.get("FLASK_SAML_SETTINGS_PATH", os.path.join(os.getcwd(), "saml"))


def build_saml_request():
    url_data = urlparse(request.url)
    is_https = request.headers.get("X_FORWARDED_PROTO") == "https" or request.scheme == "https"
    return {
        "https": "on" if is_https else "off",
        "http_host": request.host,
        "server_port": url_data.port,
        "script_name": request.path,
        "get_data": request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        "post_data": request.form.copy(),
    }


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_SETTINGS_PATH)
    return auth
