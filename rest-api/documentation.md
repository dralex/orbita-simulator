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

* **model** - the name of the calculation model;
* **mission** - the name of the particular mission.

Return codes:

* 200 - ok.

Return value in JSON format:

* **devices** - the list of available devices for the mission;
* **start_height** - the mission start height range;
* **program** - the mission default program (if available);
* **need_construction** - the boolean value if probe construction is required;
* **probe_radius** - what type of radius input is availabler for the mission, variants:
 * **none** - radius cannot be changed;
 * **internal** - internal radius need to be set;
 * **both** - the both internal and external radius need to be set.

Return value is the mission parameters list in XML format.

### Example:

Request: `GET /parameters`

Arguments:

* model: `planets`
* mission: `Moon`

Response: `{'devices': ['camera', 'generator', 'moon_damper', 'transmitter', 'diagn', 'cpu', 'engine_g', 'fueltank_large'], 'need_construction': False, 'probe_radius': 'none', 'program': "\n\t  t_off = # CALCULATE AND SET t_off\nstart_angle = # CALCULATE AND SET start_angle\n\nprobe.engine_set_angle('ERD1', start_angle)\nprobe.set_device_state('ERD1', STATE_ON)\nengine = True\n\nprobe.set_device_period('D1', 10)\n\nwhile probe.run():\n    t = probe.cpu_get_flight_time()\n    if engine and t >= t_off:\n        probe.set_device_state('ERD1', STATE_OFF)\n        engine = False\n        continue\n\n        ", 'start_height': [45000.0, 55000.0]}`

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

## GET /sample

Obtain the default probe XML for the mission.

Run the calculation on the sever. Arguments:

* **model** - the name of the calculation model;
* **mission** - the name of the particular mission.

Return codes:

* 200 - ok.

Return value is the probe sample in XML format.

### Example:

Request: `GET /sample`

Arguments:

* model: `planets`
* mission: `Moon`

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
