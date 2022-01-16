#region "Imports"
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from flask_restplus.apidoc import apidoc
#endregion

#region "Local imports"
from DomApi.config import default_specs, DumpEnvironmentConfig, SyncEnvironmentConfig
from DomApi.monitor import logger, exceptions_monitored, SetupLogger
#endregion

#region "Flask init"

#def SetupFlaskApp():

# make sure we've synced ENV vars
SyncEnvironmentConfig()

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
    #doc=f"{default_specs['apiUrlPrefix']}",
    description=default_specs["apiDescription"],
    version=default_specs["apiVersion"],
    title=default_specs["appTitle"],
)
flask_app.register_blueprint(blueprint) #, url_prefix=f"{default_specs['apiUrlPrefix']}")

# using a namespace allows for more expressive routing syntax within the REST wrapper
ns = app.namespace("api", description=default_specs["appTitle"])

#return flask_app, blueprint, ns

#flask_app, blueprint, ns = SetupFlaskApp()

#endregion


##############################################################################################
#region "Flask endpoint"


#simple model to enable direct entry in the "try it now" feature of the Swagger-UI and provide some context for the data structure
order_data = ns.model(
    "order_data", 
    {
        "eventAt": fields.String(description="Submission timestamp, ISO 8901 format", required=False),
        "storeState": fields.String(description="JSON dict containing store-level state data ", required=False),
        "storeOrders": fields.String(description="JSON array of dict items, one for each pizza being ordered.  Each item contains order id and when the order was placed, as an ISO timestamp", required=False),
        "storeEmployees": fields.String(description="JSON array of dict items, one for each employee available to make pizza.  Each item contains an employee id, shift start time, and shift end time.", required=False),
    },
)

@exceptions_monitored( logger ) 
@ns.route("/orders")
#@ns.doc(params={'OrdersJson': {'description': 'JSON-formatted set of orders'}})
class Endpoint(Resource):
    """
    Defines handlers for the "/orders" endpoint.  Implemented in this way because it allows easy global redefinition of a different root path for the api 
    without disturbing the definition of this endoint (assuming it would have more than one endpoint).   
    """
    #-------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        
        for k, v in kwargs.items():
            try:
                setattr(self, k, v)
            except:
                pass

        super().__init__()

    #-------------------------------------------------------------
    @ns.expect(order_data,validate=False)
    def post(self):
        """
        Flask POST endpoint to handle invocation of the Orders_API.Get_Order_Processing_Times method
        """
        payload=request.get_data()
        if payload:
            workerFn = default_specs["Orders_Endpoint_Worker_Fn"]
            result,status,message = workerFn(payload)
            if status:
                return result,200
            else:
                return {"result":result, "message":f"Error during processing: {message}"}, 500
        else:
            return {"result":"ERROR", "message":"Order submission not found."}, 400
    
#endregion

##############################################################################################
#region "Register & Run"

#-------------------------------------------------------------
def SetOrdersWorkerFn( Orders_Endpoint_Worker_Fn ):   
    default_specs["Orders_Endpoint_Worker_Fn"] = Orders_Endpoint_Worker_Fn


#-------------------------------------------------------------
@flask_app.before_first_request
def SetupWorker():
    # this should be a run-once method, but gunicorn and flask's dev server run in different sequences, 
    #  which is difficult to account for with a single piece of code, so I need to drop this in to prevent 
    #  double-execution on the dev server
    if not "setupComplete" in default_specs:
        default_specs["setupComplete"]  = True
    
        from DomApi.worker import Orders_API
        workerFn = Orders_API(**default_specs).Get_Order_Processing_Times
        
        SetOrdersWorkerFn(workerFn)
        
        #set Flask maximum post payload size
        #flask_app.config['MAX_CONTENT_LENGTH'] = default_specs["maxPostLengthBytes"]
        
        logger.critical(f"Config:\n {DumpEnvironmentConfig()}")
        

#-------------------------------------------------------------
def Run():
    SetupWorker()

    flask_app.run(debug=False, host="0.0.0.0", port=8080)
    
#-------------------------------------------------------------
if __name__ == "__main__":   
    Run()
    
#endregion

