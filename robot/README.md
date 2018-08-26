# Raspberry Pi Zero Robots
To further simulate the smart contract ability to control cars, we will use Raspberry Pi Zero robots to drive according to the smart contract's commands.
## Overview
The robots are three wheeled (two of them motorized) and can connect to WiFi networks. The robots will send to the server their coordinates and the server will prompt the smart contracts for the car's next command given the car's current poistion and orientation.
## Commands
The car's available commands are completely identical to the simulated commands and can manage and execute all of them.
## Operation
* To run the car's code run `robotMain.py`. The variable `USE_MOTOR` indicates wether or not to use the Motor HAT of the RPI Zero. Set the `USE_SERVER` variable to `False` if you only want to move the car without any server interaction.
* To run the car's code with the server interaction, run `main.py` with the variable `USE_SERVER` set to `True`. **Note:** make sure to change to `HOST` and `PORT` variables in the `robotClient.py` file according to your network settings and `server.py` file.