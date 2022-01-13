import logging, logging.handlers
from config import default_specs
from functools import wraps
import traceback

#get a reference to a logger, and optionally, add an smtp handler.
#    the parameters as-specified below are assuming an open relay that doesn't 
#    require authentication, which is not common on the open internet. expect to set up 
#    a local MTA, or add authentication
logger = logging.getLogger()
if default_specs['smtpLoggingEnabled']:
    smtp_handler = logging.handlers.SMTPHandler(
        mailhost=(default_specs["smtpServer"], default_specs["smtpServerPort"]),
        fromaddr=default_specs["smtpSource"],
        toaddrs=default_specs["smtpRecipient"],
        subject=f"[ERROR] {default_specs['appTitle']}",
    )
    logger.addHandler(smtp_handler)


#------------------------------------------------------    
def exceptions_monitored(logger):
    """
    defines a decorator that will catch, log, and rethrow all exceptions 
       raised within the decorated object.  
    """
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