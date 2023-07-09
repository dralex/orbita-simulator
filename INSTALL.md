# Installation instructions

You need Python (version 3.x) to run the simulation.

1. Install Google Protocol Buffers (https://protobuf.dev) version 3+ using snap protobuf or a distribution package.

2. Install the required libraries listed in requirements.txt using pip:

```
$ pip3 install -r requirements.txt
```

3. Run Makefile to build the chosen model:

```
$ cd models/earth
$ make
```

The Makefile builds the required Python encoders/decoders for XML documents and protocols.

4. Try to run the model with the test probes located in `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

5. Run the `simulation.py` script without arguments to see the possible command arguments.

6. To run servers-side calculator correct the config file `orbit_server.cfg` and run the server as daemon.

7. To localize the simulator messages you need to install `gettext` package and run `make messages` command. 

