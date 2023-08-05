import os

from flasksaml import FlaskSAML

app = FlaskSAML(__name__)
app.config['SECRET_KEY'] = 'onelogindemopytoolkit'
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')


@app.route('/', methods=['GET', 'POST'])
def index():
    return "You are authenticated"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
