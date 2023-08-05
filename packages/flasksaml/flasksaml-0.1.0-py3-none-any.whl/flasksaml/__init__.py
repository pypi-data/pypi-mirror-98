import os

from flask import Flask, request, redirect, session

from flasksaml.blueprint import saml_blueprint
from flasksaml.helper import build_saml_request, init_saml_auth

WHITELISTED_ENDPOINTS = os.environ.get("FLASK_SAML_WHITELISTED_ENDPOINTS", "status,healthcheck,health")


class FlaskSAML(Flask):
    @staticmethod
    def authenticate():
        req_path = request.path.strip("/")
        if req_path.startswith("saml") or req_path in WHITELISTED_ENDPOINTS.split(","):
            return

        if "samlNameId" in session:
            return
        req = build_saml_request()
        auth = init_saml_auth(req)

        return redirect(auth.login())

    def __init__(self, *args, **kwargs):
        super(FlaskSAML, self).__init__(*args, **kwargs)

        self.before_request(FlaskSAML.authenticate)
        self.register_blueprint(saml_blueprint)
