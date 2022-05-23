# Gr4vy Challnge

There are four micro-services in this repository that create a transaction workflow.

* auth-api : creates an authentication token for the transaction
* core-api : creates the transaction
* psp-connector : connects to Redis and processes the transaction messages
* router : A path-based http router that redirects to auth-api and core-api


## auth-api

The auth-api microservices takes two values, username and password to authenticate them against the users.json file that acts like a database for the purposes of this demo.

If the username/password combination is correct, it creates an authentication token that lasts for 30 seconds and is used by the core-api service


## core-api

The core-api microservice takes three values:

* currency (USD, GBP, EURO etc)
* amount
* token (take from the previous service)


If the token is correct the transaction is processed and stored in a backing service (Redis)

## psp-connector

The psp-connector processes the messages that are created from the successful transactions in Redis


## router

The router service is a path based http router that sits atop the auth-api and core-api services. It can resolve three paths. 

* the root path '/' which displays a jsonfied message about the Gr4vy challenge
* the auth path '/auth' that fetched a form with a username and password fields when the request made is a GET. When the request made is a POST it sends the username and password to the auth-api service.
* the transact path '/transact' that fetches a form with the currency, amount and token fields when the request made is a GET. When the request made is a POST it sends the currency, amount and token to the core-api service

The templates used for the forms are under /router/templates/ directory.



## Local setup

Before you start running the services you will need to install Redis in your local machine.

After Redis is install start the service so it runs on the default port `redis://127.0.0.1:6379/0`.

You will now need to run all four microservices with different ports. This can be achieved by creating service files but since im using macOS that doesn't have `systemctl` service files.

### auth-api

Navigate to the auth-api directory and set `HTTP_PORT` and `JWT_TOKEN` variables. You then need to run the `main.py` file.

You can do the above in one single command : `HTTP_PORT=5001 JWT_TOKEN=secret python main.py`

### core-api

Navigate to the core-api directory and set `HTTP_PORT` , `JWT_TOKEN` and `REDIS_URL` variables. You then need to run the `main.py` file.

You can do the above in one single command : `HTTP_PORT=5002 JWT_TOKEN=secret REDIS_URL=redis://127.0.0.1:6379/0 python main.py`

### psp-connector

Navigate to the psp-connector directory and set `HTTP_PORT` and `REDIS_URL` variables. You then need to run the `main.py` file.

You can do the above in one single command : `HTTP_PORT=5003 REDIS_URL=redis://127.0.0.1:6379/0 python main.py`


### router

Navigate to the router directory and set `HTTP_PORT`. You then need to run the `main.py`.

You can do the above in one single command : `HTTP_PORT=80 python main.py`

There are two other environment variables that can be set for the router microservice.

First is the `UI` (defaults to True). This determines whether the router will access the data by a browser form or from plain api calls using `httpie` or `postman`.

The second environment variable is `DOCKER` (defaults to False). This determines if the services are running as local service or as docker services in a docker network.

P.S Please make sure that nothing else is running on port 80 because the router service wont start

## Docker setup

The docker setup is quite easy to run. In the root directory there is a `docker-compose.yaml` file that includes all services, including Redis.

You will need to have the `docker-compose` binary installed which usually comes in when you install docker itself.

From then on its a matter of running `docker-compose up -d` to start the microservices.

They are reachable on the localhost.

### Bug in the docker implementation

The first part of the workflow works fine, it generates the authentication token given the correct credentials. The second part that writes the transaction to Redis, doesn't work because core-api tries to reach Redis in the localhost no matter what value you add in the `REDIS_URL`.

## UI vs httpie

In the router microservice there is an environment variable called `UI`. This enables data extraction from HTML forms. By default this is `True`, so this means that you can open up your browser and resolve your localhost (while the microservices are running - with or without docker) paths.

* http://localhost/
* http://localhost/auth
* http://localhost/transact

Both `/auth` and `/transact` paths accept `GET` and `POST` requests.

When `UI` is disabled you can use `httpie` in your termianl or `postman` to make the calls. i.e

```
http -v POST http://0.0.0.0/auth username=<valid username> password=<valid password>

http -v POST http://0.0.0.0/transact amount=2000 currency=GBP token=<valid token>
```

