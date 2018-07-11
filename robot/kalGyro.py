from Adafruit_BNO055 import BNO055
import time
import pykalman

dt = 0.01

F = [[1, dt, 0.5*dt**2],
     [0,  1,        dt],
     [0,  0,         1]]

H = [0, 0, 1]

Q = [[0.2,  0,     0],
     [0,  0.1,     0],
     [0,    0, 0.001]]

R = 0.001

bno = BNO055.BNO055(serial_port="/dev/serial0", rst = 18)

if not bno.begin():
    print("oops smth went wrong")
    raise

x,y,z = bno.read_linear_acceleration()

X0 = [0, 0, x]

P0 = [[0,0,    0],
      [0,0,    0],
      [0,0,0.001]]

kf = KalmanFilter(transition_matrices = F,
                  observation_matrices = H,
                  transition_covariance = Q,
                  observation_covariance = R,
                  initial_state_mean = X0,
                  initial_state_covariance = P0
                 )

fil_state_mean = x
fil_state_cova = 0

while True:
    x,y,x = bno.read_linear_acceleration()
    fil_state_means, fil_state_cova = kf.update(fil_state_mean,
                                                fil_state_cova,
                                                x
                                               )
    
    print(file_state_mean)
