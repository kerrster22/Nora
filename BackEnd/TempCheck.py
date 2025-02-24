from sense_hat import SenseHat
import time

sense = SenseHat()
while True:
  sense.clear()
  temp = sense.get_temperature()
  if temp<=5:
    colour = (255, 0, 0)
    sense.clear(colour)  # This turns all LEDs to red
  else:
    sense.clear()
  time.sleep(600) #check every 10 minutes