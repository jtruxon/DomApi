# Dom API

The Dom API provides a utility for quickly computing order completion times based on order volume and available staff, published through a RESTful interface.

## Requirements
* [Docker v.Latest](https://docs.docker.com/get-docker/)
* [Python v3.9+](https://www.python.org/downloads/release/python-390/)

## Quick Start
	docker run -d --restart=unless-stopped -p 8080:8080 truxonjm/domapi:latest
Open your browser to [http://localhost:8080](http://localhost:8080/)

![screen recording of DomApi SwaggerUI interface](https://media4.giphy.com/media/36eozbBPPIcPPhNZJc/giphy.gif)


## Setup 

### Local Execution
1. From within a blank working directory, clone a copy of this repository

	```
    git clone https://github.com/ohyeswedid/mlops-take-home.git . 
    ```

2. Create a virtual environment within this directory, using your favorite virtual environment utility.  An example using [pipenv](https://pipenv.pypa.io/en/latest/) might look like this:

	```
    pipenv install -r requirements.txt
	```

3. Run the DomApi.   
	
	```
    python -m DomApi.rest_wrapper.wrapper 
	```

4. Open your browser to [http://localhost:8080](http://localhost:8080/)

### Local Execution from PyPi
1. Create a virtual environment within this directory, using your favorite virtual environment utility.  An example using [pipenv](https://pipenv.pypa.io/en/latest/) might look like this:

	```
    pipenv install 
	```

2. Install the [DomApi](https://pypi.org/project/DomApi/) from PyPi 

	```
    pipenv install domapi
	```

3. Run the DomApi.   
	
	```
    python -m DomApi.rest_wrapper.wrapper 
	```

4. Open your browser to [http://localhost:8080](http://localhost:8080/)

### Docker Image Build 
1. Clone this repository into a blank working directory, as indicated above

2. Create a virtual environment within this directory, as indicated above

3. Build the package distribution

	```
	python setup.py sdist
	```

4. Build the docker image

	```
	docker build --rm -f "Dockerfile" -t domapi:latest . 
	```

5. Run the resulting docker container  

	```
	docker run -d --restart=unless-stopped -p 8080:8080 --env-file .env domapi:latest
	```

6. Open your browser to [http://localhost:8080](http://localhost:8080/)


## Using DomApi
As an [OpenAPI](https://swagger.io/resources/open-api/)-compliant service, the DomApi can be consumed easily by using open-source tools to create client applications in the language of your choice.  One such tool is the open source [PySwagger](https://github.com/pyopenapi/pyswagger) package for python. 

Alternatively, the service metadata, linked directly beneath the title on the homepage of the service UI, can be imported into the [Swagger Editor](https://editor.swagger.io/) online utility, which is capable of generating clients in over 50 languages.  The this metadata is found at [http://localhost:8080/swagger.json](http://localhost:8080/swagger.json), if the setup instructions above are followed.


## Configuration
This application is designed with a number of configurable values.  Given that it's targeted towards a  Docker-based runtime environment, it is designed to consume these settings environment variables within the guest OS.  

To make your custom setting visible to the application, set an environment variable using the following scheme: 
    
    {appEnvPrefix}{VARIABLE_NAME}=VALUE

For example, to override the `"validateOrder"` value, set an environment variable named `"DOM_API_VALIDATEORDER"` (note the use of **ALL UPPERCASE**).

for Windows, this would look like:

```
> SET DOM_API_VALIDATEORDER=FALSE
```

, or for Linux, this would look like:

```
$ export DOM_API_VALIDATEORDER='FALSE'
```

In practice,  this is most easily implemented through use of a `".env"`  file, which is just a list of key/value pairs separated by an `"="`.  This way, environment settings can be passed in bulk to the `docker run` command by using the `--env-file` option ([reference](https://docs.docker.com/engine/reference/commandline/run/)).


### Application Variables
| Name | Type | Default Value | Description 
|-|-|-|-|
| appEnvPrefix | string |"DOM_API_" | This prefix should be added to all environment variables intended for injection into the service.  **It cannot be modified at runtime**.
| apiUrlPrefix | string | "" | This variable can be used to change the root URL of the API. This is useful in situations where multiple services are being aggregated under a single hostname, such as a microservice cluster in Kubernetes with a single ingress. A sample value could be: `"/domapi"`
| apiVersion | string | "1.0.0" | Sets the version of the API that's published through the interface in through the metadata.
| apiTitle | string |"Dom Order API" | Sets the title of the API that's published through the interface in through the metadata.
| apiDescription | string | "" | Sets the description of the API that's published through the interface in through the metadata.
| validateOrder | boolean | True | Each submission is checked for schema validation prior to processing. This is critical for error management in an environment where there are a variety of consumers for the service, but in a tightly controlled development environment, it may be possible to safely skip the validation & gain some performance.
| orderMakeTimeSeconds | integer | 120 | The time in seconds required to assemble a single pizza.
| allowEmployeeOverTime | boolean | False | This value used for testing, not intended for production.
| preSortOrders | boolean | True | If orders can be guaranteed to come in pre-sorted chronologically, then a slight gain in performance may be achieved by setting this value to `False`, and bypassing the initial sort of submitted orders.
|loggingLevel| string | "WARNING" | Logging level for the application, can take on one of the following values: `{NOTSET,INFO,DEBUG,WARNING,ERROR,CRITICAL}`
| smtpLoggingEnabled | boolean | False | This application features global exception monitoring; this setting, in conjunction with the next four, enable application exceptions to the reflected back to a mailbox for simple alerting. **note**: there is no authentication specified, so any MTA specified below will need to behave as an open relay for this service.
| smtpServer | boolean | "" | SMTP Logging: mail server hostname or IP address
| smtpServerPort | boolean | 25 | SMTP Logging: mail server port 
| smtpSource | string | "" | SMTP Logging: source email address
| smtpRecipient | string | "" | SMTP Logging: recipient email address



# License

 **DomApi** is freely distributable under the terms of the [MIT license](LICENSE).