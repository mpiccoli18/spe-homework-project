import datetime
import queue
import matplotlib.pyplot as plt
import numpy as np

lam = 2 #Lambda for exponential distribution

class Server:
    def __init__(self):
        self.isBusy = False
        self.currentEvent = None
    
    def isServerBusy(self):
        return self.isBusy
    
    def assignEvent(self, event):
        self.currentEvent = event
        self.isBusy = True
    
    def releaseEvent(self):
        self.currentEvent = None
        self.isBusy = False
    
    def getCurrentEvent(self):
        return self.currentEvent

class Event:
    def __init__(self, eventType, timestamp):
        self.eventType = eventType
        self.timestamp = timestamp
        self.next = None

class EventQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def addEventbasedOnTimestamp(self, event):
        if self.front is None:
            self.front = event
            self.rear = event
        else:
            current = self.front
            previous = None

            while current is not None and current.timestamp <= event.timestamp:
                previous = current
                current = current.next
            
            if previous is None:
                event.next = self.front
                self.front = event
            else:
                previous.next = event
                event.next = current
            
            if current is None:
                self.rear = event
        
        self.size += 1

    def removeEvent(self):
        if self.front is None:
            return None
        
        removedEvent = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None
        self.size -= 1
        return removedEvent
    
    def getFront(self):
        return self.front

    def getRear(self):
        return self.rear

    def isEmpty(self):
        return self.front is None
    
    def getSize(self):
        return self.size
    
class randomGenerator:
    def __init__(self):
        self.rng = np.random.default_rng()
    
    def generateUniformRandNum(self):
        return self.rng.random()

    def generateExponentialRandNum(self):
        return self.rng.exponential(1/lam)

def main():
    print("Simulation started at: ", datetime.datetime.now())
    print("Intializing event queue, server and random number generator...")
    eventQueue = EventQueue()
    rng = randomGenerator()
    
    uniform = rng.generateUniformRandNum()
    print("Uniform number generated: ", uniform)

    exponential = rng.generateExponentialRandNum()
    print("Exponential number generated: ", exponential)
    

    

    







if __name__ == "__main__":
    main()