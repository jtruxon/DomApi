#region "Imports"
from flask import Flask, Blueprint
from flask_restplus import Api
from flask_restplus.apidoc import apidoc
#endregion

#region "Local imports"
from DomApi.config import default_specs
#endregion

#region "Flask init"

# create a Flask app, prepend a url prefix if necessary, set up swagger ui metadata
apidoc.url_prefix = default_specs["apiUrlPrefix"]
flask_app = Flask(__name__)

# ProxyFix is a well-known bugfix that allows flask to run properly behind a reverse proxy
#   ref: https://werkzeug.palletsprojects.com/en/0.14.x/contrib/fixers/
from werkzeug.middleware.proxy_fix import ProxyFix
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_proto=1, x_host=1)

# using a blueprint allows the swagger-ui docs to confinue functioning when the api is 
#   shifted to a new URL root
blueprint = Blueprint("api", __name__, url_prefix=f"{default_specs['apiUrlPrefix']}")
app = Api(
    app=blueprint,
    #doc=f'/doc/',
    description=default_specs["apiDescription"],
    version=default_specs["apiVersion"],
    title=default_specs["appTitle"],
)
flask_app.register_blueprint(blueprint)

# using a namespace allows for more expressive routing syntax within the REST wrapper
ns = app.namespace("api", description=default_specs["appTitle"])

#endregion