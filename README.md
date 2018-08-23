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
Cars can be controled by setting a spped for them, then starting to call commands in a loop. The cars can only move or rotate once, every time a call has been made to one of their command functions.
* `MOV`
    * moves the car in its current direction `velocity` units. doesn't take any parameters. the faster the car the more it moves.
* `ROT <angle>`
    * rotates the car towards the desired `angle`. should be called until the desired `angle` has been acheived and the car stops rotating. **Note:** when `ROT 90` is called the car will rotate until it reached 90 degrees of the X-axis, it does not rotate 90 degrees regardles of it's current angle.
* `MOVXY <x> <y>`
    * Moves the car to a specified (x, y) value. The car will first rotate to achieve the correct angle, then will move forward until it's position is (x, y). **Note:** you dont need to change the commands until the given point is reached, the `MOVXY` command internaly changes it commands.
* `RAD <radius> <angle>`
    * Moves the car in an arch with a radius of `radius` until it reaches the desired `angle`.
* `WAIT <time>`
    * Makes the car stay in place for a given amount of calls to `car.decInterval()` (which should be called once every iteration of the main loop). The `WAIT` command changes the internal state of the car to `car.stop` to ensure the car can't move.