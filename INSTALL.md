# Linux Installation Guide

You need Python (version 3.x) to run the simulator.

1. First of all, update all system packages and install python3.

```
$ sudo apt update && sudo apt update
$ sudo apt install python3
$ sudo apt install python3-pip
```

2. Install Google Protocol Buffers (https://protobuf.dev) version 3.

```
$ sudo apt install protobuf-compiler
```

3. Install the required libraries listed in `requirements.txt` file using `pip`:

```
$ pip3 install -r requirements.txt
```

4. Select the model you are interested in and run the Makefile to build the chosen model:

```
$ cd models/earth
$ make unix
```

The Makefile builds the required Python encoders/decoders for XML documents and protocols.

5. Try to run the model with the test probes located in `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

6. Run the `simulation.py` script without arguments to see the possible command arguments.

7. To run servers-side calculator correct the config file `orbit_server.cfg` and run the server as daemon.

8. To localize the simulator messages you need to install `gettext` package and run `make messages` command. 


# MacOS Installation Guide


1. First of all, install the brew package manager (https://brew.sh/index_ru).

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install python3.

```
$ brew install python3
```

3. Install Google Protocol Buffers (https://protobuf.dev) version 3.

```
$ brew install protobuf
```

4. Install the required libraries listed in `requirements.txt` file using `pip`:

```
$ pip3 install -r requirements.txt
```

5. Select the model you are interested in and run the Makefile to build the chosen model:

```
$ cd models/earth
$ make unix
```

The Makefile builds the required Python encoders/decoders for XML documents and protocols.

6. Try to run the model with the test probes located in `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

7. Run the `simulation.py` script without arguments to see the possible command arguments.

8. To run servers-side calculator correct the config file `orbit_server.cfg` and run the server as daemon.

9. To localize the simulator messages you need to install `gettext` package and run `make messages` command. 



# Windows Installation Guide


1. First of all, install python3 (https://www.python.org/downloads/windows).

2. Install the make tool (we execute all commands in the PowerShell window).
```
$ Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
$ choco install make
```

3. Install Google Protocol Buffers (https://protobuf.dev) version 3.

3.1 Install the win64/win32 archive from the official repository (https://github.com/protocolbuffers/protobuf/releases).

3.2 Unzip the archive in a location convenient for you.

3.3 Copy the path to the protoc.exe file, which will be in the archive.

3.4. Add the path to the environment settings file (in the PATH field)



4. Install the required libraries listed in `requirements.txt` file using `pip`:

```
$ pip3 install -r requirements.txt
```

5. Select the model you are interested in and run the Makefile to build the chosen model:

5.1 if you are running the simulator for the first time:
```
$ cd models/earth
$ make win
```
5.2 If you are running the simulator again or make some changes:
```
$ cd models/earth
$ make clean_win
$ make win
```

The Makefile builds the required Python encoders/decoders for XML documents and protocols.

6. Try starting the test apparatus from the `probes` directory:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

7. Run the `simulation.py` script without arguments to see the possible command arguments.

8. To run servers-side calculator correct the config file `orbit_server.cfg` and run the server as daemon.

9. To localize the simulator messages you need to install `gettext` package and run `make messages` command. 
