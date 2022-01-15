#region "Imports"
import os
from distutils import util
from pkg_resources import resource_filename
#endregion

# grab a reference to the location of our package resources folder
resources_filepath = resource_filename(__name__, '../resources')

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
    "orderMakeTimeSeconds": 120,
    "allowEmployeeOverTime": False,
    "preSortOrders": True,
    "smtpServer": "smtp.gmail.com",
    "smtpServerPort": 25,
    "smtpSource": "noreply@jamestruxon.com",
    "smtpRecipient": "contact@jamestruxon.com",
    "smtpLoggingEnabled": False,
    "orderSchemaFilename": f"{resources_filepath}/request_schema.json",
    "orderSchema":"",
    # "defaultTimeZone": -5,  #assuming each orders submission operates within the same timezone.
    "loggingLevel": "INFO"
}

#---------------------------------------
def SyncEnvironmentConfig():
    #update default specs from environment, where supplied, using prefix defined above

    # ignore these keys during ENV override.  
    ignoreEnvOverrides = ["appEnvPrefix","orderSchemaFilename"]

    # step through all keys in the default specs, look for correspondingly named environment variables and typecast them
    # to match the types in the default config
    for k in default_specs.keys():
        
        if k in ignoreEnvOverrides: continue
        
        try:
            valType = type(default_specs[k])
            envValue = os.environ[f"{default_specs['appEnvPrefix']}{k.upper()}"]

            if valType is not bool:
                default_specs[k] = valType(envValue)
            else:
                default_specs[k] = valType(util.strtobool(envValue))
        except KeyError: 
            # we do not want to raise an error if the given key hasn't been specified at the ENV level
            pass
        except:
            # raise all other exceptions 
            raise
        
#dump 
def DumpEnvironmentConfig():
    return "\n".join([f'{item[0]}: {item[1]}' for item in  default_specs.items()])
    

#endregion