from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port="/dev/serial0" ,rst = 18)

cal_x = []
cal_y = []
cal_z = []

min_x = max_x = avg_x = None
min_y = max_y = avg_y = None
min_z = max_z = avg_z = None

def calibrate(t):
    global cal_X
    global cal_y
    global cal_z

    global max_x
    global min_x
    global avg_x

    global max_y
    global min_y
    global avg_y

    global max_z
    global min_z
    global avg_z
   
    for i in range(1000):
        x, y, z = bno.read_linear_acceleration()
        cal_x.append(x)
        cal_y.append(y)
        cal_z.append(z)
        
        time.sleep(t / 1000)

    min_x = min(cal_x)
    max_x = max(cal_x)
    avg_x = sum(cal_x) / len(cal_x)

    min_y = min(cal_y)
    max_y = max(cal_y)
    avg_y = sum(cal_y) / len(cal_y)

    min_z = min(cal_z)
    max_z = max(cal_z)
    avg_z = sum(cal_z) / len(cal_z)

    print(max_x, min_x, avg_x, max_y, min_y, avg_y, max_z, min_z, avg_z)

if not bno.begin():
    print("error, maybe connection is bad?")

sysCal = gyroCal = magCal = accCal = 0

# some possible calibrations
# [227, 255, 207, 255, 230, 255, 97, 1, 119, 253, 178, 2, 255, 255, 1, 0, 3, 0, 232, 3, 111, 4]

print("fully calibrated!")

carX = 0
carvX = 0
carY = 0
carvY = 0
caraX = 0
caraY = 0
carAngle = 0

input("are you ready?")
WAIT = 0.01

calibrate(4)

while True:
    heading, roll, pitch = bno.read_euler()
    x, y, z = bno.read_linear_acceleration()
    #print("\nheading: "+str(heading)+", roll: "+str(roll)+", pitch: "+str(pitch))
    #print("X: "+str(x/100)+", Y: "+str(y/100)+", Z: "+str(z/100)+"")
    
    if not (x < max_x and x > min_x):
        carvX += ((x + caraX + avg_x) / 2) * WAIT
        

    if y > 0:
        carvY += round(y, 3) * WAIT
    else:
        carvY += round(y, 3) * WAIT

    carX += carvX * WAIT
    carY += carvY * WAIT 
    
    print("{0:0.3F} {1:0.3F} {2:0.3F}".format(caraX, carvX, carX))

    caraX = x
    caraY = round(y, 3)
    
    carAnle = heading
    #print("CAR:")
    #print(carX, carY, heading)
    time.sleep(WAIT)

