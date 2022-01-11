# import pytest
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource
from flask_restplus.apidoc import apidoc
import requests, datetime, time, math, json, os
import traceback
from functools import wraps
import logging, logging.handlers


# --------------------------------------------------------------------------------------------------------
default_specs = {
    "appEnvPrefix": "DOMINOS_API_",
    "appTitle": "Dominos Order API",
    "apiUrlPrefix": "",
    "apiVersion": "0.0",
    "apiDescription": "",
    "validateOrder": True,
    "throwErrors": True,
    "orderMakeTimeSeconds": 120,
    "employeeOvertime": False,
    "preSortOrders": True,
    "smtpServer": "smtp.gmail.com",
    "smtpServerPort": 25,
    "smtpSource": "noreply@jamestruxon.com",
    "smtpRecipient": "contact@jamestruxon.com",
}

#update default specs from environment, where supplied, using prefix defined above
for k in default_specs.keys():
    try:
        default_specs[k] = os.environ[f"{default_specs['appEnvPrefix']}{k.upper()}"]
    except:
        pass

# --------------------------------------------------------------------------------------------------------
smtp_handler = logging.handlers.SMTPHandler(
    mailhost=(default_specs["smtpServer"], default_specs["smtpServerPort"]),
    fromaddr=default_specs["smtpSource"],
    toaddrs=default_specs["smtpRecipient"],
    subject=f"[ERROR] {default_specs["appTitle"]}",
)
logger = logging.getLogger()
logger.addHandler(smtp_handler)


# --------------------------------------------------------------------------------------------------------
def exceptions_monitored(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except Exception as e:
                issue = {
                    "result": "Error",
                    "function": f"{func.__name__}",
                    "message": repr(e),
                    "traceback": traceback.format_exc(),
                }
                logger.exception(msg="[ERROR]", extra=issue)
            raise

        return wrapper

    return decorator


# --------------------------------------------------------------------------------------------------------
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

ns = app.namespace("api", description="Main APIs")



##################################################################################################################################################################################
@exceptions_monitored(logger)
class Orders_API:
    def __init__(self, **kwargs):
        # override default values with any kwargs passed in
        for k, v in kwargs.items():
            try:
                setattr(self, k, v)
            except:
                pass

    def Get_Order_Processing_Times(self, orders):
        """
          * convert dates to timestamp objects (staff, orders)
		* add staff to queue, key = startTime
		* sort orders (if not disabled)
		* while orders exist
                - pop order, pop staff member
                - if (startTime + order_cycle_time) > endTime, skip.  else:
                - order_completion = max(first_availability, order time) + order_cycle_time
                - order_duration = order_completion - order_placed
                - staff.first_availability += order_cycle_time
                - push staff member to queue
		* compile output

        """
        from queue import PriorityQueue
        staff = PriorityQueue()
        pass


##################################################################################################################################################################################
@exceptions_monitored( logger ) 
@ns.route("/orders")
@ns.doc(params={'representation_set_id': {'description': 'Representation Set ID'}})
class Endpoint(Resource):
	def __init__(self, *args, **kwargs):
		self.api = Orders_API(**kwargs)

		for k, v in kwargs.items():
			try:
				setattr(self, k, v)
			except:
				pass
		self.default_specs= default_specs
		super().__init__()

	def post(self):
		if request.get_data():
			payload=request.get_data()
			return self.api.Get_Order_Processing_Times(payload), 200
		else:
			return {"result":"Error", "message":"Configuration data was not received successfully."}
	


if __name__ == "__main__":
    flask_app.run(debug=False, host="0.0.0.0", port=8080)
