# Orbita-Simulator RESTful API

This document contains RESTful API for the Orbita-Simulator simulation
program for probe space stations from orbital missions to landing.

The web-based API contains stataless calls which implement the basic
functions of the Orbita-Simulation calculation server. The HTTPS-based
authorization is recommended due to the lack of authentication
functions in this API.

The list of methods:

## GET /server

Obtain the basic calculation server information. The
method has no arguments.

Return codes:

* 200 - ok.

Return value in JSON format:

* server version;
* supported calculation models;
* number of calculating tasks (status: working).

### Example:

Request: `GET /server`

Response: `{"version": "1.0", "models": ["planets", "planets_gravity"], "tasks": 0}`

## GET /parameters

Obtain the list of available mission parameters.

Run the calculation on the sever. Arguments:

* **model** - the name of the calculation model.

Return codes:

* 200 - ok.

Return value is the mission parameters list in XML format.

### Example:

Request: `GET /parameters`

Arguments:

* model: `planets`

Response: `{"data": "...XML BLOB..."}`

## GET /devices

Obtain the list of available devices.

Run the calculation on the sever. Arguments:

* **model** - the name of the calculation model.

Return codes:

* 200 - ok.

Return value is the devices list in XML format.

### Example:

Request: `GET /devices`

Arguments:

* model: `planets`

Response: `{"data": "...XML BLOB..."}`

## POST /calculation

Run the calculation on the sever. Arguments:

* **model** - the name of the calculation model;
* **xml** - the XML document BLOB with the calculation parameters;

Return codes:

* 200 - ok;
* 404 - model with the name specified not found.

Return value:

* **id** - the unique identifier of the calculation task;

### Example:

Request: `POST /calculation`

Arguments:

* model: `planets_gravity`
* xml: `...XML BLOB...`

Response: `{"id": "1734334695570590"}`

## GET /status

Check the status of the calculation task. Arguments:

* **model** - the name of the calculation model;
* **id** - the unique identifier of the calculation, contains only digits (0-9);

Return codes:

* 200 - ok;
* 400 - bad format of the calculation identifier;
* 404 - model with the name specified not found.

Return value contains the status string:

* **not found** - the task with the id was not found;
* **working** - the task is being calculated;
* **completed** - the calculaton was completed.

Example:


## GET /result

Get result of the completed calculation. Argument:

* **model** - the name of the calculation model;
* **id** - the unique identifier of the calculation, contains only digits (0-9);

Return codes:

* 200 - ok;
* 400 - bad format of the calculation identifier;
* 404 - model with the name specified not found OR the task was not completed actually.

Return value contains list of URLs with the calculation results in
JSON format:

* **xml** - path to the short xml with results;
* **logfile** - path to the calculation log;
* **images** - list of paths to the parameters graph files.

### Example:

Request: `GET /parameters`

Arguments:

* model: `planets`
* id: `1734423422805180`

Response: `{'xml': '/static/results/planets_gravity/1734423422805180-short.xml', 'images': ['/static/images/planets_gravity/1734423422805180-As.png', '/static/images/planets_gravity/1734423422805180-Ac.png', '/static/images/planets_gravity/1734423422805180-Vx-Vy.png', '/static/images/planets_gravity/1734423422805180-H.png'], 'log': '/static/results/planets_gravity/1734423422805180-result.log'}`
