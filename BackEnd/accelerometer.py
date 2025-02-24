from sense import SenseHat
sense = SenseHat()
white = (255, 255, 255)
sense.clear(white)
red = (255, 0, 0)

while True:
    acceleration = sense.get_accelerometer_raw()
    x_accel = acceleration['x']
    y_accel = acceleration['y']
    z_accel = acceleration['z']
    total_acceleration = x_accel + y_accel + z_accel

    if total_acceleration >= 10:
        sense.clear(red)
        break
    else:
        sense.clear(white)