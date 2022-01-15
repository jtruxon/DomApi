#region "Imports"
import logging, logging.handlers
#endregion

#region "Local imports"
from DomApi.config import default_specs
#endregion

#region "Logging init"

#------------------------------------------------------    
def AddSMTPHandler_FromConfig(logger):
        smtp_handler = logging.handlers.SMTPHandler(
            mailhost=(default_specs["smtpServer"], default_specs["smtpServerPort"]),
            fromaddr=default_specs["smtpSource"],
            toaddrs=default_specs["smtpRecipient"],
            subject=f"[ERROR] {default_specs['appTitle']}",
        )
        logger.addHandler(smtp_handler)

#------------------------------------------------------    
def AddStdOutHandler(logger):
    import sys
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

#------------------------------------------------------    
def SetLoggingLevel_FromConfig(logger):
    levels = {
        "critical":logging.CRITICAL,        
        "error":logging.ERROR,        
        "warning":logging.WARNING,        
        "info":logging.INFO,        
        "debug":logging.DEBUG,        
        "notset":logging.NOTSET,        
    }
    try:
        logger.setLevel(levels[default_specs["LoggingLevel"].tolower()])
    except KeyError: pass
    except: raise

# get a reference to a logger, and optionally, add an smtp handler.
#    the parameters as-specified below are assuming an open relay that doesn't 
#    require authentication, which is not common on the open internet. expect to set up 
#    a local MTA, or add authentication
logger = logging.getLogger()

AddStdOutHandler(logger)
SetLoggingLevel_FromConfig(logger)

if default_specs['smtpLoggingEnabled']: 
    AddSMTPHandler_FromConfig(logger)
    
#endregion


#------------------------------------------------------    
#region "Exception decorator declaration"
def exceptions_monitored(logger):
    """
    defines a decorator that will catch, log, and rethrow all exceptions 
       raised within the decorated object.  
    """
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            import traceback
            
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

#endregion
