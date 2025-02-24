from sense_hat import SenseHat
import time

EvilTemp = 5
sense = SenseHat()

while True:
  sense.clear()
  temp = sense.get_temperature()
  if temp<=EvilTemp:
    for x in range (10):  #10 iterations of 30 seconds = 5 min
      time.sleep(30)    #wait 30sec between each check
      if temp<=EvilTemp:
        lowTemp = True
      else:
        lowTemp = False
  if lowTemp == True:   #if after 5 min last check still reads True trigger emergency protocol
    colour = (255, 0, 0)
    sense.clear(colour) # This turns all LEDs to red (will be swapped for emergency protocol)
  else:
    sense.clear()
  time.sleep(600)       #check every 10 minutes