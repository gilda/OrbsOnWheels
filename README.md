# OrbsOnWheels
OrbsOnWheels is a project dedicated to develop a blockchain driven self driving car (blockchain driven car?)
The project uses raspberry pi zeros to control robot cars through a smart contract on the [ORBS network](orbs.com). 
## Module features
* Simulation of cars using [matplotlib.](https://matplotlib.org/)
* Simulation of cars, drawing cars by data that clients send.
* Simulation of cars, drawing cars by data that clients send according to commands recieved from the server.
## Usage
1. To run the simulation of cars without any communication: run `main.py` and set the global variable `USE_SERVER = False`. This will run the simulation with the given commands: `cmd0` `cmd1` and `cmd2` to control all cars.

2. To run the Simulation with data straight from the client (without the server letting the client know which command it should run): run `main.py` with the global variable `USE_SERVER = True`, `SEND_COMMAND` in `server.py` should be `False` and `USE_SERVER_COMMAND` in `network/client.py` should be `False`. after running `main.py` you can run the `client.py` but be sure to change any network addresses that might change for you.  

3. To run the simulation of cars with the server letting the clients which commands to execute: run `main.py` with the global variable `USE_SERVER = True`, `SEND_COMMAND` in `server.py` should be `True` and `USE_SERVER_COMMAND` in `network/client.py` should be `True`.

**Note:** configutarion 1 will run all the commands from the `main.py` file, 2 will run commands from the `network/client.py` file and 3 will run commands from the `server.py` file.
## Car command reference
TODO