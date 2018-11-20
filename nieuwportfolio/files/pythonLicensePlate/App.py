from Camera import Camera
from Logger import Logger
from Led import Led
from Sonic import Sonic
import time

#init
camera = Camera()
led = Led()
logger = Logger()
sonic = Sonic()

#start
logger.info("Starting program")

#red led
logger.info("Turning red led on")
led.turnLedOn("red")


#start capturing
condition = True
logger.info("Reading distance")
try:
    while condition:
        distance = sonic.getDistance()
        logger.debug("Reading distance => {dist}".format(dist=distance))
        time.sleep(1)
        if distance >= 30 and distance <= 120:
            camera.captureImage()
            camera.recognizePlate()
except KeyboardInterrupt:
    logger.info("Stopping reading distance")

#close
logger.info("Releasing resources camera")
camera.close()

#end
logger.info("Closing program")
led.turnLedOff("red")
led.turnLedOff("green")