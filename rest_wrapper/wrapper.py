#region "Imports"
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from rest_wrapper import ns, flask_app
#endregion

#region "Local imports"
from config import default_specs
from monitor import logger, exceptions_monitored
#endregion

##############################################################################################
#region "Flask endpoint"

#simple model to enable direct entry in the "try it now" feature of the Swagger-UI and provide some context for the data structure
order_data = ns.model(
    "order_data", 
    {
        "eventAt": fields.String(description="Submission timestamp, ISO 8901 format", required=True),
        "storeState": fields.String(description="JSON dict containing store-level state data ", required=True),
        "storeOrders": fields.String(description="JSON array of dict items, one for each pizza being ordered.  Each item contains order id and when the order was placed, as an ISO timestamp", required=True),
        "storeEmployees": fields.String(description="JSON array of dict items, one for each employee available to make pizza.  Each item contains an employee id, shift start time, and shift end time.", required=True),
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
        from api.worker import Orders_API
        payload=request.get_data()
        if payload:
            api = Orders_API(**default_specs)
            result,status,message = api.Get_Order_Processing_Times(payload)
            if status:
                return result,200
            else:
                return {"result":result, "message":f"Error during processing: {message}"}, 500
        else:
            return {"result":"ERROR", "message":"Order submission not found."}, 400
    
#endregion

##############################################################################################
#region "Flask run"
def Run():   
    flask_app.run(debug=False, host="0.0.0.0", port=8080)
    
if __name__ == "__main__":   
    Run()
#endregion

