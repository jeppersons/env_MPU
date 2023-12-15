import board
import adafruit_mpu6050
import time
import matplotlib.pyplot as plt

# Create I2C object using the default I2C pins
i2c = board.I2C()

# Initialize MPU6050 object
mpu = adafruit_mpu6050.MPU6050(i2c)

# Lists to store accelerometer data
acc_x = []
acc_y = []
acc_z = []

# Plot setup
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
line_x, = ax.plot(acc_x, label='X')
line_y, = ax.plot(acc_y, label='Y')
line_z, = ax.plot(acc_z, label='Z')
ax.legend()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration')
plt.show()

# Data collection duration (seconds)
duration = 10

start_time = time.time()
while time.time() - start_time < duration:
    # Read accelerometer data
    acceleration = mpu.acceleration
    acc_x.append(acceleration[0])
    acc_y.append(acceleration[1])
    acc_z.append(acceleration[2])

    # Update plot
    line_x.set_ydata(acc_x)
    line_y.set_ydata(acc_y)
    line_z.set_ydata(acc_z)
    ax.relim()  # Recalculate limits
    ax.autoscale_view(True, True, True)  # Rescale axis
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Wait for a short period
    time.sleep(0.1)
