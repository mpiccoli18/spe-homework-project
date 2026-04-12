import datetime
import queue
import matplotlib.pyplot as plt
import numpy as np

lam = 1 #Lambda for exponential distribution
mu = 2  #Mu for exponential distribution

class Server:
    def __init__(self):
        self.busy = False
        self.currentEvent = None
    
    def isBusy(self):
        return self.busy
    
    def assignEvent(self, event):
        self.currentEvent = event
        self.busy = True
    
    def releaseEvent(self):
        self.currentEvent = None
        self.busy = False
    
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

    def generateExponentialRandNum(self, num):
        return self.rng.exponential(1/num)

def arrival(currentEvent, currentTime, eventQueue, server, rng, waitingQueue):
        nextArrivalTime = currentTime + rng.generateExponentialRandNum(lam)
        nextArrivalTimeEvent = Event("ARRIVAL", nextArrivalTime)
        eventQueue.addEventbasedOnTimestamp(nextArrivalTimeEvent)

        if server.isBusy():
            waitingQueue.append(currentTime)
        else:
            server.assignEvent(currentEvent)
            departureTime = currentTime + rng.generateExponentialRandNum(mu)
            departureEvent = Event("DEPARTURE", departureTime)
            eventQueue.addEventbasedOnTimestamp(departureEvent)

def departure(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, mu):
    arrival = server.getCurrentEvent()
    systemTime = currentTime - arrival.timestamp
    totalTimeSpent.append(systemTime)

    if len(waitingQueue) == 0:
        server.releaseEvent()
    else:
        nextArrivalTime = waitingQueue.pop(0)
        server.assignEvent(Event("ARRIVAL", nextArrivalTime))

        serviceTime = rng.generateExponentialRandNum(mu)
        departureTime = currentTime + serviceTime
        departureEvent = Event("DEPARTURE", departureTime)
        eventQueue.addEventbasedOnTimestamp(departureEvent)

def confidenceInterval(totalTimeSpent):
    mean = np.mean(totalTimeSpent)
    standardDeviation = np.std(totalTimeSpent)
    n = len(totalTimeSpent)
    z = 1.96
    marginOfError = z * (standardDeviation / np.sqrt(n))
    lowerBound = mean - marginOfError
    upperBound = mean + marginOfError
    print(f"Confidence Interval: [{lowerBound}, {upperBound}]")

def plot(totalTimeSpent):
    
    averageRun = []
    sum = 0
    for i, time in enumerate(totalTimeSpent):
        sum += time
        averageRun.append(sum / (i + 1))

    average = 1 / (mu - lam)
    plt.plot(averageRun, label="Running Average")
    plt.axhline(y=average, color='r', linestyle='-', label="Theoretical Average")
    plt.xlabel("Number of Packets Processed")
    plt.ylabel("Average Time in System")
    plt.legend()
    plt.show()

def main():
    print("Simulation started at: ", datetime.datetime.now())
    print("Intializing event queue, server and random number generator...")
    eventQueue = EventQueue()
    rng = randomGenerator()
    server = Server()
    currentTime = 0.0
    waitingQueue = []
    totalTimeSpent = []
    
    uniform = rng.generateUniformRandNum()
    print("Uniform number generated: ", uniform)

    exponential = rng.generateExponentialRandNum(lam)
    print("Exponential number generated: ", exponential)

    firstEvent = Event("ARRIVAL", exponential)
    eventQueue.addEventbasedOnTimestamp(firstEvent)
    print("First event added to the queue with timestamp: ", exponential)

    MAX = 1000000

    while not eventQueue.isEmpty():
        currentEvent = eventQueue.removeEvent()
        currentTime = currentEvent.timestamp
        
        if currentTime > MAX:
            break

        if currentEvent.eventType == "ARRIVAL":
            arrival(currentEvent, currentTime, eventQueue, server, rng, waitingQueue)
        
        elif currentEvent.eventType == "DEPARTURE":
            departure(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, mu)

    
    print("Simulation ended at: ", datetime.datetime.now())
    print("Calculating confidence interval and plotting results...")
    confidenceInterval(totalTimeSpent)
    plot(totalTimeSpent)
    return 0


if __name__ == "__main__":
    main()