class Car():

    def __init__(self,plateNumber=None,color=None,brand=None):
        
        #plate
        if plateNumber == None:
            self.plateNumber = ""
        else:
            self.plateNumber = plateNumber
        
        #color
        if color == None:
            self.color = "skin"
        else:
            self.color = color
        
        #brand
        if brand == None:
            self.brand = "human"
        else:
            self.brand = brand

    def getPlateNumber(self):
        return self.plateNumber

    def getColor(self):
        return self.color
    
    def getBrand(self):
        return self.brand