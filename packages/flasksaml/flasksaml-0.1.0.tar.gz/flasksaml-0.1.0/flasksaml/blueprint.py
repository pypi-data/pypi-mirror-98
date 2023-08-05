from flask import Blueprint, request, redirect, session, make_response
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from flasksaml.helper import build_saml_request, init_saml_auth

saml_blueprint = Blueprint("saml", __name__, url_prefix="/saml")


@saml_blueprint.route("/slo")
def slo():
    """The endpoint to trigger SP-initiated SLO request"""
    req = build_saml_request()
    auth = init_saml_auth(req)

    name_id = session["samlNameId"] if "samlNameId" in session else None
    session_index = session["samlSessionIndex"] if "samlSessionIndex" in session else None
    name_id_format = session["samlNameIdFormat"] if "samlNameIdFormat" in session else None
    name_id_nq = session["samlNameIdNameQualifier"] if "samlNameIdNameQualifier" in session else None
    name_id_spnq = session["samlNameIdSPNameQualifier"] if "samlNameIdSPNameQualifier" in session else None

    return redirect(
        auth.logout(
            name_id=name_id,
            session_index=session_index,
            nq=name_id_nq,
            name_id_format=name_id_format,
            spnq=name_id_spnq,
        )
    )


@saml_blueprint.route("/acs", methods=["GET", "POST"])
def acs():
    """The endpoint to process SAML Authentication Response"""
    req = build_saml_request()
    auth = init_saml_auth(req)

    request_id = session["AuthNRequestID"] if "AuthNRequestID" in session else None
    auth.process_response(request_id=request_id)

    errors = auth.get_errors()
    if len(errors) > 0 and auth.get_settings().is_debug_active():
        return auth.get_last_error_reason()

    if "AuthNRequestID" in session:
        del session["AuthNRequestID"]

    session["samlUserdata"] = auth.get_attributes()
    session["samlNameId"] = auth.get_nameid()
    session["samlNameIdFormat"] = auth.get_nameid_format()
    session["samlNameIdNameQualifier"] = auth.get_nameid_nq()
    session["samlNameIdSPNameQualifier"] = auth.get_nameid_spnq()
    session["samlSessionIndex"] = auth.get_session_index()
    self_url = OneLogin_Saml2_Utils.get_self_url(req)

    if "RelayState" in request.form and self_url != request.form["RelayState"]:
        return redirect(auth.redirect_to(request.form["RelayState"]))


@saml_blueprint.route("/sls", methods=["GET", "POST"])
def sls():
    """The endpoint to process SLO request coming from IdP"""
    req = build_saml_request()
    auth = init_saml_auth(req)

    request_id = session["LogoutRequestID"] if "LogoutRequestID" in session else None
    url = auth.process_slo(request_id=request_id, delete_session_cb=session.clear)

    errors = auth.get_errors()
    if len(errors) > 0 and auth.get_settings().is_debug_active():
        return auth.get_last_error_reason()

    if url is not None:
        return redirect(url)


@saml_blueprint.route("/metadata")
def metadata():
    req = build_saml_request()
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers["Content-Type"] = "text/xml"
    else:
        resp = make_response(", ".join(errors), 500)
    return resp
