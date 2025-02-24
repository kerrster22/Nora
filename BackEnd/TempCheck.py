from sense_hat import SenseHat
import time

EvilTemp = 5
sense = SenseHat()

while True:
  sense.clear()
  temp = sense.get_temperature()
  if temp<=EvilTemp:
    lowTempCount = 0

    for x in range (10):    #10 iterations of 30 seconds = 5 min
      time.sleep(30)        #wait 30sec between each check
      temp = sense.get_temperature
      if temp<=EvilTemp:
        lowTempCount +=1
    
    if lowTempCount >= 6:   #if detected under threshhold more than x times run emergency protocol
        colour = (225, 0, 0)#red
        sense.clear(colour)
    else:
        sense.clear()
else:
    sense.clear()
    time.sleep(600)         #check every 10 minutes
