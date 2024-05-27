# Parking Lot In Python  Working code

# Requirements
# The parking lot should have multiple levels, each level with a certain number of parking spots.
# The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
# Each parking spot should be able to accommodate a specific type of vehicle.
# The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
# The system should track the availability of parking spots and provide real-time information to customers.
# The system should handle multiple entry and exit points and support concurrent access.


# Domain classes
# parking Lot , Parking level , Parking spots
# Vehicles
# Entry , Exit -- multiple
# system
# Dashboard


# use case diagram 
    # - User
 
#  System 
#  - The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits
#  - The system should handle multiple entry and exit points and support concurrent access
#  - The system should track the availability of parking spots and provide real-time information to customers.

from abc import ABC
from enum import Enum

#this will be a singleton class
class ParkingLot():
    _instance=None
    
    def __new__(cls,*args, **Kwargs):
        if cls._instance is None:
            cls._instance = super(ParkingLot, cls).__new__(cls)
        return cls._instance
    
    def __init__(self,name, address):
        self._instantiated=False
        if self._instantiated == False:
            self.__name= name
            self.__address = address
            self.__levels = []    #private
            self._instantiated = True
            
    def addLevel(self,level):
        self.__levels.append(level)
    
    def parkVehicle(self,vehicle):
        for currentLevel in self.__levels:
            if currentLevel.parkVehicle(vehicle):
                return True
        return False
    
    def unparkVehicle(self, vehicle):
        for currLevel in self.__levels:
            if currLevel.unparkVehicle(vehicle):
                return True
        return False
    
    def displayAvailibility(self):
        for currLevel in self.__levels:
            currLevel.displayAvailability()


class ParkingLevel:
    
    def __init__(self, levelNum , spots):
        self.__levelNum = levelNum
        self.__parkingSpots = []
        for i in range(0, spots):
            self.__parkingSpots.append(Spot(i,VehicleType.BIKE ))
    
    def parkVehicle(self,vehicle):
        print("got Vehicle", vehicle)
        for spot in self.__parkingSpots:
            if spot.isAvailable() and (spot.getVehicleType()==vehicle.getVehicleType()):
                spot.parkVehicle(vehicle)
                return True
        return False
    
    def unparkVehicle(self,vehicle):
        for spot in self.__parkingSpots:
            if not spot.isAvailable() and spot.getParkedVehicle() == vehicle:
                spot.unparkVehicle(vehicle)
                return True
        return False
    
    def displayAvailability(self):
        print(f"level {self.__levelNum} Availibility")
        for spot in self.__parkingSpots:
            print(f"{spot.getSpotNumber()}{spot.isAvailable()}")

            

class Spot:
    def __init__(self,spotNumber, spotType):
        self.__spotNumber = spotNumber
        self.__spotType = spotType
        self.__parkedVehicle = None
        
    def isAvailable(self):
        if self.__parkedVehicle == None:
            return True
        return False
    
    def parkVehicle(self, vehicle):
        print("vehicle type", vehicle.getVehicleType())
        print("__spotType", self.__spotType)
        if (self.isAvailable() and vehicle.getVehicleType()==self.__spotType):
            self.__parkedVehicle = vehicle
        else:
            print("Invalid Vehicle Type or spot occupied")
    
    def unparkVehicle(self, vehicle):
        self.__parkedVehicle= None
    
    def getParkedVehicle(self):
        return self.__parkedVehicle
    
    def getSpotNumber(self):
        return self.__spotNumber
    
    def getVehicleType(self):
        return self.__spotType
    
class VehicleType(Enum):
    CAR=1
    TRUCK=2
    BIKE=3
    

class Vehicle(ABC):
    def __init__(self, number, type):
        self._number = number
        self._type = type
    
    def getVehicleType(self):
        return self._type
        
    def __str__(self):
        return f"Vehicle(_number={self._number}, _type={self._type})"


class Car(Vehicle):
    def __init__(self, number):
        super().__init__(number, VehicleType.CAR)

    
class BIKE(Vehicle):
    def __init__(self, number):
        super().__init__(number, VehicleType.BIKE)
    
    
class Truck(Vehicle):
    def __init__(self, number):
        super().__init__(number, VehicleType.TRUCK)
        


parkingLot = ParkingLot("Ankit's Parking Lot" , "F301")
level1 = ParkingLevel(1, 3)
level2 = ParkingLevel(2, 3)
level3 = ParkingLevel(3, 3)

parkingLot.addLevel(level1)
parkingLot.addLevel(level2)
parkingLot.addLevel(level3)

parkingLot.displayAvailibility()

bike1 = BIKE(123)
bike2 = BIKE(456)
bike3 = BIKE(789)
bike4 = BIKE(596)
parkingLot.parkVehicle(bike1)
parkingLot.parkVehicle(bike2)
parkingLot.parkVehicle(bike3)
parkingLot.parkVehicle(bike4)
parkingLot.unparkVehicle(bike1)

parkingLot.displayAvailibility()




