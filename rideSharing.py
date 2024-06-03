# The ride sharing service should allow passengers to request rides and drivers to accept and fulfill those ride requests.
# Passengers should be able to specify their pickup location, destination, and desired ride type (e.g., regular, premium).
# Drivers should be able to see available ride requests and choose to accept or decline them.
# The system should match ride requests with available drivers based on proximity and other factors.
# The system should calculate the fare for each ride based on distance, time, and ride type.
# The system should handle payments and process transactions between passengers and drivers.
# The system should provide real-time tracking of ongoing rides and notify passengers and drivers about ride status updates.


from abc import ABC
from enum import Enum
from collections import deque
import random


class RideType(Enum):
    Regular=1
    Premium=2

class DriverStatus(Enum):
    available=1
    notAvailable=2
    InRide=3

class PaymentStatus(Enum):
    PENDING=1
    COMPLETED=2
    FAILED=3

class RideStatus(Enum):
    REQUESTED = 1
    ACCEPTED = 2
    IN_PROGRESS = 3
    COMPLETED = 4
    CANCELLED = 5

class Ride:
    def __init__(self,source,destination,passenger):
        self.source=source
        self.destination=destination
        self.passenger= passenger
        self.driver=None
        self.eta=None
        self.actualTime=None
        self.fare=None
        self.status= RideStatus["REQUESTED"]

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_source(self):
        return self.source

    def set_source(self, value):
        self.source = value

    def get_destination(self):
        return self.destination

    def set_destination(self, value):
        self.destination = value

    def get_passenger(self):
        return self.passenger

    def set_passenger(self, value):
        self.passenger = value

    def get_driver(self):
        return self.driver

    def set_driver(self, value):
        self.driver = value

    def get_eta(self):
        return self.eta

    def set_eta(self, value):
        self.eta = value

    def get_actualTime(self):
        return self.actualTime

    def set_actualTime(self, value):
        self.actualTime = value

    def get_fare(self):
        return self.fare

    def set_fare(self, value):
        self.fare = value

class Person:
    def __init__(self):
        self.name = name
        self.email = email

class Passengers(Person):

    def __init__(self,name, email, currLocation):
        self.__name=name
        self.__email=email
        self.__currLocation= currLocation

    # A ride object will be created and pushed  to a current pool
    # def requestRide(currLocation, destination, type):
    #     r1=Ride(self.currLocation, destination, {name: self.name, email:self.email}, Ride.Regular)
    #     driverRidesPool.updateRidePool(r1)
    #     #Store this in a pool of requests
    #     return r1
    
    def getName(self):
        return self.__name
    
    def getemail(self):
        return self.__email
    
    def getLocation(self):
        return self.__currLocation
    
class Drivers(Person):
    
    def __init__(self, name, email, currLocation, status, licensePlate):
        self.__name=name
        self.__email= email
        self.__currLocation = currLocation
        self.__status = status
        self.licennsePlate= licensePlate

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_email(self):
        return self.__email

    def set_email(self, value):
        self.__email = value

    def get_currLocation(self):
        return self.__currLocation

    def set_currLocation(self, value):
        self.__currLocation = value

    def get_status(self):
        return self.__status

    def set_status(self, value):
        self.__status = value

    def get_licennsePlate(self):
        return self.licennsePlate

    def set_licennsePlate(self, value):
        self.licennsePlate = value


#this should be singleton class
class RideService:
    __instance=None

    def __new__(cls, *args, **Kwargs):
        if cls.__instance==None:
            cls.__instance = super(RideService , cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.instantiated = False
        if self.instantiated == False:
            self.__passengers = []
            self.__drivers = []
            self.__rides = []
            self.instantiated = True

    def get_requestedRides(self):
        return self.__rides

    def addPassenger(self, passenger):
        self.__passengers.append(passenger)
    
    def addDriver(self,driver):
        self.__drivers.append(driver)

    def requestRide(self , passenger, source, destination):
        r1 =Ride(passenger.getLocation(), destination, passenger)
        self.__rides.append(r1)
        self.notifyDrivers(r1)

    def acceptRide(self,ride,driver):
        print("RideStatus.REQUESTED", ride.get_status())
        if ride.get_status() == RideStatus.REQUESTED:
            ride.set_driver(driver)
            ride.set_status(RideStatus.ACCEPTED)
            driver.set_status(DriverStatus.InRide)
            self.notifyPassenger(ride)


    def notifyDrivers(self,ride):
        for driver in self.__drivers:
            if driver.get_status()==DriverStatus.available:
                if abs(driver.get_currLocation() - ride.passenger.getLocation()<=5):
                    print("Notifying Driver", driver.get_email())

    
    
    def notifyPassenger(self,ride):
        passenger = ride.get_passenger()
        match ride.get_status():
            case RideStatus.ACCEPTED:
                print("Your ride has been accepted , Driver on the way")
            case RideStatus.IN_PROGRESS:
                print("Your ride is in progress")
            case RideStatus.COMPLETED:
                print("Your ride is completed")
                print("Tour fare", ride.get_fare())
            case RideStatus.CANCELLED:
                print("Your ride has been CANCELLED")

    def notifyDriver(self,ride):
        drivr = ride.get_driver()
        if drivr != None:
            match (ride.get_status()):
                case "COMPLETED":
                    print("Total fare to collect", ride.get_fare())
                case "CANCELLED":
                    print("Ride CANCELLED")
    
    

    def startRide(self,ride):
        if ride.get_status()==RideStatus.ACCEPTED:
            ride.set_status(RideStatus.IN_PROGRESS)
            self.notifyPassenger(ride)
    
    def completeRide(self,ride):
        if ride.get_status()==RideStatus.IN_PROGRESS:
            ride.set_status(RideStatus.COMPLETED)
            ride.get_driver().set_status(DriverStatus.available)
            totalFare = self.calculateFare(ride)
            ride.set_fare(totalFare)
            self.processPayment()
            self.notifyPassenger(ride)
            self.notifyDriver(ride)

    def cancelRide(self,ride):
         if ride.get_status() == (RideStatus.ACCEPTED or RideStatus.REQUESTED):
            ride.set_status(RideStatus.CANCELLED)
            if not ride.get_driver() == None:
                ride.get_driver().set_status(DriverStatus.available)
            self.notifyPassenger(ride)
            self.notifyDriver(ride)
    
    def calculateFare(self,ride):
        baseFare = 2
        parKmFare = 1.5
        perMinFare=0.25

        distance = self.calculateDistance(ride.get_source(), ride.get_destination())
        time = self.calculateTime(ride.get_source(), ride.get_destination())

        return baseFare + (distance * parKmFare) + (time* perMinFare)
    
    def calculateDistance(self,source,destination):
        return random.random()
    
    def calculateTime(self,source,destination):
        distance = self.calculateDistance(source, destination)
        return (distance//30)*60

    def processPayment(self):
        return
    


if __name__=="__main__":

    rideSvc =  RideService()

    p1 = Passengers("Ankit", "ankitkhowal.nitb@gmail.com", 10)
    p2 = Passengers("Gunjan", "gka@gmail.com", 20)
    rideSvc.addPassenger(p1)
    rideSvc.addPassenger(p2)

    d1 = Drivers("driver1", "d1@gmail.com", 12, DriverStatus.available, "ka-03" )
    d2 = Drivers("driver2", "d2@gmail.com", 22, DriverStatus.available, "ka-05" )

    rideSvc.addDriver(d1)
    rideSvc.addDriver(d2)


    rideSvc.requestRide(p1, p1.getLocation(), 50)
    rides = rideSvc.get_requestedRides()
    currRide = rides.pop()

    rideSvc.acceptRide(currRide , d1)

    rideSvc.startRide(currRide)

    rideSvc.completeRide(currRide)

    rideSvc.requestRide(p2, p2.getLocation(), 70)

    rides = rideSvc.get_requestedRides()
    currRide = rides.pop()
    rideSvc.acceptRide(currRide , d2)

    rideSvc.cancelRide(currRide)
