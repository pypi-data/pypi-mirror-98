# Flask SAML

A Flask wrapper that implements SAML Service Provider (SP) functionalities. A marriage between
[Flask](https://github.com/pallets/flask) and [python3-saml](https://github.com/onelogin/python3-saml).

## Installation

```
pip install flasksaml
```

## Usage

### Set SAML parameters

For SAML SSO to work, you need to set certain parameters, particularly regarding the SAML SP & IdP. These
definitions are set in `settings.json` and `advanced_settings.json`. For more information, please consult
the documentation of [python3-saml](https://github.com/onelogin/python3-saml).

After you configured `settings.json` & `advanced_settings.json`, set the location of the directory
containing those 2 files in the `FLASK_SAML_SETTINGS_PATH` environment variable.

### Create Flask App

Create your Flask application using the FlaskSAML class as such:

```python
from flasksaml import FlaskSAML

app = FlaskSAML(__name__)

# Set a cryptographically secure secret key. This secret key is used to sign session cookies. Failure to
# to do so might enable tampering of session cookies
# https://flask.palletsprojects.com/en/1.1.x/config/?highlight=secret_key#SECRET_KEY
app.config["SECRET_KEY"] = "so-so-secret"
```


## Environment Variables

```python

# Comma-separated string of URL paths that should not require authentication
# Default: "status,healthcheck,health"
FLASK_SAML_WHITELISTED_ENDPOINTS: "status,healthcheck,health"

# The location of directory containing settings.json & advanced_settings.json
# Defaults to current working directory
FLASK_SAML_SETTINGS_PATH: ""
```
