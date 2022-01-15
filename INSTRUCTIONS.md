# Dominos API

The Domino's API provides a utility for quickly computing order completion times based on order volume and available staff, published through a RESTful interface.

## Requirements
* [Docker v.Latest](https://docs.docker.com/get-docker/)
* [Python v3.9+](https://www.python.org/downloads/release/python-390/)

## Quick Start
	docker run -d --restart=unless-stopped -p 8080:8080 truxonjm/domapi:latest
Open your browser to [http://localhost:8080](http://localhost:8080/)

![screen recording of DomApi SwaggerUI interface](https://i.ibb.co/4FdkXTJ/DOMAPI-Swagger-UI.gif)


## Setup 

### Local Execution
1. From within a blank working directory, clone a copy of this repository
	`git clone https://github.com/ohyeswedid/mlops-take-home.git . `

2. Create a virtual environment within this directory, using your favorite virtual environment utility.   Example using [pipenv](https://pipenv.pypa.io/en/latest/): 
	`pipenv install -r requirements.txt`

3. Run the DomApi.   
	`python -m DomApi.rest_wrapper.wrapper `

4. Open your browser to [http://localhost:8080](http://localhost:8080/)


### Docker Image Build 
1. From within a blank working directory, clone a copy of this repository
	`git clone https://github.com/ohyeswedid/mlops-take-home.git . `

2. Create a virtual environment within this directory, using your favorite virtual environment utility.   Example using [pipenv](https://pipenv.pypa.io/en/latest/): 
	`pipenv install -r requirements.txt`

3. Build the package distribution
	`python setup.py sdist`

4. Build the docker image
	`docker build --rm -f "Dockerfile" -t domapi:latest . `

5. Run the resulting docker container  
	`docker run -d --restart=unless-stopped -p 8080:8080 --env-file .env domapi:latest`

6. Open your browser to [http://localhost:8080](http://localhost:8080/)


### Using DomApi
To learn more about this package, please refer to our [readthedocs.io](https://rancher.com/docs/rancher/v2.6/en/) site.


# License

 **DomApi** is freely distributable under the terms of the [MIT license](LICENSE).