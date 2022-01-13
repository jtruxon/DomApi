#region "Imports"
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from flask_restplus.apidoc import apidoc
from math import ceil
#endregion

#region "Local imports"
from config import default_specs
#endregion

#region "Flask init"
#create a Flask app, prepend a url prefix if necessary, set up swagger ui metadata
apidoc.url_prefix = default_specs["apiUrlPrefix"]
flask_app = Flask(__name__)
from werkzeug.middleware.proxy_fix import ProxyFix
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_proto=1, x_host=1)

blueprint = Blueprint("api", __name__, url_prefix=f"{default_specs['apiUrlPrefix']}")
app = Api(
    app=blueprint,
    #doc=f'/doc/',
    description=default_specs["apiDescription"],
    version=default_specs["apiVersion"],
    title=default_specs["appTitle"],
)
flask_app.register_blueprint(blueprint)

ns = app.namespace("api", description=default_specs["appTitle"])
#endregion