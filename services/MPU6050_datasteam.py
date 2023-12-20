import board
import adafruit_mpu6050
import time
import math

# Create I2C object using the default I2C pins
i2c = board.I2C()

# Initialize MPU6050 object
mpu = adafruit_mpu6050.MPU6050(i2c)

# Infinite loop to continuously read and print accelerometer data
while True:
    # Reading accelerometer data from the MPU6050
    acceleration = mpu.acceleration
    xAccel=acceleration[0]
    yAccel=acceleration[1]
    zAccel=acceleration[2]
    
    # Clamp zAccel to avoid domain errors
    zAccel = max(min(zAccel, 1), -1)

    theta=math.acos(zAccel)
    thetaDeg=theta/2/math.pi*360
    
    # Format the output for Thonny's Plotter (X, Y, Z values separated by spaces)
    #print(f"{acceleration[0]:.5f} {acceleration[1]:.5f} {acceleration[2]:.5f}")
    #print(f"{xAccel:.5f} {yAccel:.5f} {zAccel:.5f}")
    #print('x: ',xAccel,'    ', 'y: ',yAccel, '    ','z: ',zAccel,' ')
    print('Tilt Angle: ',thetaDeg,' Degress')


    # Wait for a short interval before the next reading
    time.sleep(.1)
