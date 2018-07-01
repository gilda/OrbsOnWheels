from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port="/dev/serial0" ,rst = 18)

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
carAngle = 0

input("are you ready?")
WAIT = 0.01
while True:
    heading, roll, pitch = bno.read_euler()
    x, y, z = bno.read_linear_acceleration()
    #print("\nheading: "+str(heading)+", roll: "+str(roll)+", pitch: "+str(pitch))
    #print("X: "+str(x/100)+", Y: "+str(y/100)+", Z: "+str(z/100)+"")
    
    if x > 0:
        carvX += x/100 * WAIT if x/100 > 0.01 else 0
    else:
        carvX += x/100 * WAIT if x/100 < -0.01 else 0
    
    if y > 0:
        carvY += y/100 * WAIT if y/100 > 0.01 else 0
    else:
        carvY += y/100 * WAIT if y/100 < -0.01 else 0
    
    print(carvX, carvY)

    carX += carvX * WAIT
    carY += carvY * WAIT

    carAnle = heading
    #print("CAR:")
    #print(carX, carY, heading)
    time.sleep(WAIT)

