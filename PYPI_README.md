
The Dom API provides a utility for quickly computing order completion times based on order volume and available staff, published through a RESTful interface.

## Installing
	$ pip install domapi
	$ python -m DomApi.rest_wrapper.wrapper 

Open an incognito browser to [http://localhost:8080](http://localhost:8080/)


## Using DomApi
As an [OpenAPI](https://swagger.io/resources/open-api/)-compliant service, the DomApi can be consumed easily by using open-source tools to create client applications in the language of your choice.  One such tool is the open source [PySwagger](https://github.com/pyopenapi/pyswagger) package for python. 

Alternatively, the service metadata, linked directly beneath the title on the homepage of the service UI, can be imported into the [Swagger Editor](https://editor.swagger.io/) online utility, which is capable of generating clients in over 50 languages.  This metadata is found at [http://localhost:8080/swagger.json](http://localhost:8080/swagger.json), if the setup instructions above are followed.


## Configuration
This application is designed with a number of configurable values.  Given that it's targeted towards a  Docker-based runtime environment, it is designed to consume these settings through environment variables within the guest OS.  

To make your custom setting visible to the application, set an environment variable using the following scheme: 
    
    {appEnvPrefix}{VARIABLE_NAME}=VALUE

For example, to override the `"validateOrder"` value, set an environment variable named `"DOM_API_VALIDATEORDER"` (note the use of **ALL UPPERCASE**).

for Windows, this would look like:

```
> SET DOM_API_VALIDATEORDER=FALSE
```

, or for Linux, this would look like:

```
$ export DOM_API_VALIDATEORDER="FALSE"
```

### Application Variables
| Name | Type | Default Value | Description 
|-|-|-|-|
| appEnvPrefix | string |"DOM_API_" | This prefix should be added to all environment variables intended for injection into the service.  **It cannot be modified at runtime**.
| apiUrlPrefix | string | "" | This variable can be used to change the root URL of the API. This is useful in situations where multiple services are being aggregated under a single hostname, such as a microservice cluster in Kubernetes with a single ingress. A sample value could be: `"/domapi"`
| apiVersion | string | "1.1.0" | Sets the version of the API that's published through the interface in through the metadata.
| apiTitle | string |"Dom Order API" | Sets the title of the API that's published through the interface in through the metadata.
| apiDescription | string | "" | Sets the description of the API that's published through the interface in through the metadata.
| validateOrder | boolean | True | Each submission is checked for schema validation prior to processing. This is critical for error management in an environment where there are a variety of consumers for the service, but in a tightly controlled development environment, it may be possible to set this value to `False`, and safely skip the validation to gain some performance.
| orderMakeTimeSeconds | integer | 120 | The time in seconds required to assemble a single pizza.
| allowEmployeeOverTime | boolean | False | This value used for testing, not intended for production.
| preSortOrders | boolean | True | If orders can be guaranteed to come in pre-sorted chronologically, then a slight gain in performance may be achieved by setting this value to `False`, and bypassing the initial sort of submitted orders.
|loggingLevel| string | "WARNING" | Logging level for the application, can take on one of the following values: `{NOTSET,INFO,DEBUG,WARNING,ERROR,CRITICAL}`
| smtpLoggingEnabled | boolean | False | This application features global exception monitoring; this setting, in conjunction with the next four, enables application exceptions to the reflected back to a mailbox for simple alerting. **note**: there is no authentication specified, so any MTA specified below will need to behave as an open relay for this service.
| smtpServer | boolean | "" | SMTP Logging: mail server hostname or IP address
| smtpServerPort | boolean | 25 | SMTP Logging: mail server port 
| smtpSource | string | "" | SMTP Logging: source email address
| smtpRecipient | string | "" | SMTP Logging: recipient email address



# License

 **DomApi** is freely distributable under the terms of the [MIT license](LICENSE).