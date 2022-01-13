#region "Imports"
import os
#endregion

#------------------------------------------------------    
#region "Configuration init"

# these values will be available to the api worker, and may be overridden by setting 
# environment variables with the format: {appEnvPrefix}{VARIABLE NAME}, e.g. to 
# override the smtpServerPort, call "set DOMINOS_API_SMTPSERVERPORT=[value]" in Windows, 
# or "export DOMINOS_API_SMTPSERVERPORT=[value]" in Linux. Do not override appEnvPrefix;
# this won't throw errors, but it will likely cause unpredictable value write-in behavior
default_specs = {
    "appEnvPrefix": "DOMINOS_API_",
    "appTitle": "Dominos Order API",
    "apiUrlPrefix": "",
    "apiVersion": "0.0",
    "apiDescription": "",
    "validateOrder": True,
    "throwErrors": True,
    "orderMakeTimeSeconds": 120,
    "allowEmployeeOverTime": False,
    "preSortOrders": True,
    "smtpServer": "smtp.gmail.com",
    "smtpServerPort": 25,
    "smtpSource": "noreply@jamestruxon.com",
    "smtpRecipient": "contact@jamestruxon.com",
    "smtpLoggingEnabled": False,
    "orderSchemaFilename":"request_schema.json",
    "orderSchema":"",
    "defaultTimeZone": -5
}

#update default specs from environment, where supplied, using prefix defined above
for k in default_specs.keys():
    try:
        default_specs[k] = os.environ[f"{default_specs['appEnvPrefix']}{k.upper()}"]
    except: pass
    
#endregion