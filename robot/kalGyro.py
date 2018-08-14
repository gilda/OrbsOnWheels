from Adafruit_BNO055 import BNO055
import time
from pykalman import KalmanFilter, UnscentedKalmanFilter

dt = 0.01

F = [[1, dt, 0.5*dt**2],
     [0,  1,        dt],
     [0,  0,         1]]

H = [0, 0, 1]

Q = [[0.2,  0,    0],
     [0,  0.1,    0],
     [0,    0, 0.01]]

R = 0.01


bno = BNO055.BNO055(serial_port="/dev/serial0", rst=18)

if not bno.begin():
    print("oops smth went wrong")
    raise

cal_x = []
cal_y = []
cal_z = []

minx = maxx = avgx = None
miny = maxy = avgy = None
minz = maxz = avgz = None


def calibrate(t):
    global cal_x
    global cal_y
    global cal_z
    global minx
    global maxx
    global avgx
    global miny
    global maxx
    global avgy
    global minz
    global maxz
    global avgz
    for i in range(t):
        x, y, z = bno.read_linear_acceleration()
        cal_x.append(x)
        cal_y.append(y)
        cal_z.append(z)

    minx = min(cal_x)
    maxx = max(cal_x)
    avgx = sum(cal_x) / len(cal_x)

    miny = min(cal_y)
    maxy = max(cal_y)
    avgy = sum(cal_y) / len(cal_y)

    minz = min(cal_z)
    maxz = max(cal_z)
    avgz = sum(cal_z) / len(cal_z)


calibrate(1000)

x, y, z = bno.read_linear_acceleration()

if not(x < maxx and x > minx):
    x = x + avgx
else:
    x = 0

X0 = [0, 0, x]

P0 = [[0, 0,     0],
      [0, 0,     0],
      [0, 0,     R]]

kf = KalmanFilter(transition_matrices=F,
                  observation_matrices=H,
                  transition_covariance=Q,
                  observation_covariance=R,
                  initial_state_mean=X0,
                  initial_state_covariance=P0
                  )

t = 0

while True:
    x, y, z = bno.read_linear_acceleration()
    if t == 0:
        fil_state_mean = X0
        fil_state_cova = P0
    else:
        if not (x < maxx and x > minx):
            x = x + avgx
        else:
            x = 0

        pfil_state_mean = fil_state_mean
        fil_state_mean, fil_state_cova = (
            kf.filter_update(fil_state_mean, fil_state_cova, x))
        fil_state_mean = (pfil_state_mean + fil_state_mean) / 2

    #print("{0:0.3F} {1:0.3F}".format(x, fil_state_mean1[0]))
    print("{0:0.3F} {1:0.3F} {2:0.3F}".format(
        fil_state_mean[2], fil_state_mean[1], fil_state_mean[0]))
    t += 1
