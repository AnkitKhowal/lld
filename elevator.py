# Domain classes
# Elevator system -- Entry point , shows the usage of elevators
# Elevator controller-- manages multiple elevators
# Elevators -- indivisual elevators
# requests -- request for movement of elevator
# Floors
# Users --> 
# Buttons
# InternalButtons
# ExternalButtons
# Algorithm to optimize movement - Movement strategy

from enum import Enum
from abc import ABC
import math

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class ElevatorSystem:
    
    def __init__(self):
        self.__elevatorcontroller = ElevatorController(3)
    
    def getElevatorController(self):
        return self.__elevatorcontroller
        
    
class ElevatorController:
    def __init__(self, numberOfElevators):
        self.__elevators = []
        for i in range(0,numberOfElevators):
            self.__elevators.append(ElevatorCar(i , 5))
    
    def requestElevator(self, source , destination):
        optimalElevator = self.findOptimalElevator(source, destination)
        print("optimal Elevator id :", optimalElevator.getID())
        optimalElevator.addRequest(Request(source, destination))
    
    def findOptimalElevator(self, source, destination):
        optimalElevator=None
        minDistance = float("inf")
        
        for elevator in self.__elevators:
            distance =  abs(elevator.getCurrentFloor() - source)
            if distance < minDistance:
                minDistance = distance
                optimalElevator = elevator
                
        return optimalElevator
    
    def printElevatorFloors(self):
        for ele in self.__elevators:
            print("Elevator Number ", ele.getID())
            print("on floor", ele.getCurrentFloor())

class ElevatorCar():
    
    def __init__(self, id, capacity):
        self.__id =id
        self.__capacity = capacity
        self.__currentFloor = 1
        self.__currentDirection = Direction.UP
        self.__requests = []
    
    def addRequest(self, request):
        self.__requests.append(request)
        self.processRequests()
            
    def processRequests(self):
        while(len(self.__requests)>0):
            currRequest = self.__requests.pop()
            destination = currRequest.getDestination()
            if self.__currentFloor < destination:
                print("Moving up")
                self.__currentFloor = destination
                self.__currentDirection = Direction.UP
            else:
                 print("Moving down")
                 self.__currentFloor = destination
                 self.__currentFloor = Direction.DOWN
    
    def getCurrentFloor(self):
        return self.__currentFloor
    
    def getID(self):
        return self.__id
        
    
class Request:
    
    def __init__(self, source, destination):
        self.__source=source
        self.__destination=destination
    
    def getSource(self):
        return self.__source
    
    def getDestination(self):
        return self.__destination
        

system = ElevatorSystem()
controller = system.getElevatorController()
controller.requestElevator(5, 10)
controller.requestElevator(3, 7)
controller.requestElevator(5, 8)
controller.printElevatorFloors()

    
    
