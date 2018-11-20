#imports
import time
from picamera import PiCamera
import json
import requests
import base64
import os
#own classes
from Car import Car
from Database import Database
from Logger import Logger
from Led import Led

class Camera():

    def __init__(self):
        self.db = Database()
        self.camera = PiCamera()
        self.led = Led()
        self.logger = Logger()

    def captureImage(self):
        self.logger.info("Taking image from camera")
        self.camera.capture('/home/pi/Documents/Projectweek-IOT/images/nummerplaat.jpg')

    def recognizePlate(self):
        #init
        params = (
            ('image_url', 'http://cdn.bmwblog.com/wp-content/uploads/2015/12/2015-BMW-320d-xDrive-Touring-test-drive-67-750x500.jpg'),
            ('secret_key', 'sk_5abc2ff5d5317e3b42d656aa'),
            ('recognize_vehicle', '1'),
            ('country', 'eu'),
            ('return_image', '0'),
            ('topn', '1'),
        )

        #convert image to base64
        self.logger.info("Encoding image to base64 for request")
        encodedString = ""
        with open("/home/pi/Documents/Projectweek-IOT/images/nummerplaat.jpg", "rb") as image:
            encodedString = base64.b64encode(image.read())

        #delete image
        self.logger.info("Deleting image of plate number")
        os.remove("/home/pi/Documents/Projectweek-IOT/images/nummerplaat.jpg")

        #request
        self.logger.info("Making request for recognizing the plate")
        response = requests.post('https://api.openalpr.com/v2/recognize_bytes', params=params,data=encodedString)

        #parse json
        self.logger.info("Saving car details")
        car = self.parseResponse(response.json())

        if(car.getPlateNumber() == ""):
            self.logger.error("No plate number detected")
            return

        self.logger.succes("plate number that is being checked => " + car.getPlateNumber())
        #check db
        if(self.db.nummerplaatControle(car.getPlateNumber())):
            self.led.turnLedOff("red")
            self.led.turnLedOn("green")
            time.sleep(2)
            self.led.turnLedOff("green")
            time.sleep(0.5)
            self.led.turnLedOn("red")


    def parseResponse(self,jsonData):
        if not jsonData['results']:
            return Car()

        parsedJson = jsonData['results'][0]

        return Car(parsedJson['plate'])

    def close(self):
        self.camera.close()