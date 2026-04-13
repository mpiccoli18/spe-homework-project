import datetime
import matplotlib.pyplot as plt
import numpy as np
import math

lam = 4.8       #Lambda for exponential distribution
lam2 = 0.1      #Lambda for exercise 2: lam2 << M
mu = 5          #Mu for exponential distribution

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

    def generateExponentialRandNum(self, num):
        return self.rng.exponential(1/num)
    
    def generateCustomServiceTime(self, M):
        while True:
            x = self.rng.uniform(0, 6)
            y = self.rng.uniform(0, M)
            
            if y <= newServiceTime(x):
                return x

# Arrival function defined for exercise 1
def arrivalEx1(currentEvent, currentTime, eventQueue, server, rng, waitingQueue):
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

# Arrival function defined for exercise 2
def arrivalEx2(currentEvent, currentTime, eventQueue, server, rng, waitingQueue, M):
        nextArrivalTime = currentTime + rng.generateExponentialRandNum(lam2)
        nextArrivalTimeEvent = Event("ARRIVAL", nextArrivalTime)
        eventQueue.addEventbasedOnTimestamp(nextArrivalTimeEvent)

        if server.isBusy():
            waitingQueue.append(currentTime)
        else:
            server.assignEvent(currentEvent)
            departureTime = currentTime + rng.generateCustomServiceTime(M)
            departureEvent = Event("DEPARTURE", departureTime)
            eventQueue.addEventbasedOnTimestamp(departureEvent)

# Departure function defined for exercise number 1
def departureEx1(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, mu):
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

# Departure function defined for exercise number 2
def departureEx2(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, M):
    arrival = server.getCurrentEvent()
    systemTime = currentTime - arrival.timestamp
    totalTimeSpent.append(systemTime)

    if len(waitingQueue) == 0:
        server.releaseEvent()
    else:
        nextArrivalTime = waitingQueue.pop(0)
        server.assignEvent(Event("ARRIVAL", nextArrivalTime))
        serviceTime = rng.generateCustomServiceTime(M)
        departureTime = currentTime + serviceTime
        departureEvent = Event("DEPARTURE", departureTime)
        eventQueue.addEventbasedOnTimestamp(departureEvent)


def confidenceInterval(totalTimeSpent, batch=500):
    data = totalTimeSpent[1000:]
    num = len(data) // batch
    batchMean = []
    
    for i in range(num):
        batches = data[i * batch : (i + 1) * batch]
        batchMean.append(np.mean(batches))
    

    mean = np.mean(batchMean)
    standardDeviation = np.std(batchMean, ddof=1)
    n = len(batchMean)
    z = 1.96
    marginOfError = z * (standardDeviation / np.sqrt(n))
    lowerBound = round(mean - marginOfError, 4)
    upperBound = round(mean + marginOfError, 4)
    print("Confidence Interval is between ", lowerBound, " and ", upperBound)
    return lowerBound, upperBound

def plot(totalTimeSpent, confidence, isFirstEx = True):
    
    averageRun = []
    sum = 0
    for i, time in enumerate(totalTimeSpent):
        sum += time
        averageRun.append(sum / (i + 1))
    
    plt.plot(averageRun, color='b', label="Running Average")
    
    CI = confidence
    plt.axhline(y=CI[0], color = 'r', linestyle="--", label= "Confidence Interval")
    plt.axhline(y=CI[1], color = 'r', linestyle="--")

    if isFirstEx:
        average = 1 / (mu - lam)
        plt.axhline(y=average, color='g', linestyle='--', label="Theoretical Average")
    
    plt.xlim(None, len(totalTimeSpent))
    plt.xlabel("Number of Packets Processed")
    plt.ylabel("Average Time in System")
    plt.legend()
    plt.show()

def newServiceTime(x):
    if x < 0 or x > 6:
        return 0
    elif x == 3:
        return 1.0
    else:
        return abs((math.sin(math.pi * (x - 3))) / (math.pi * (x - 3)))

def getAvgServiceTime(M, rng):
    totalNum = 10000
    sum = 0
    for _ in range(totalNum):
        sum += rng.generateCustomServiceTime(M)
    
    avg = round(sum / totalNum, 4)
    lambdaMax = round(1 / avg, 4)
    print("Estimated average service time:", avg)
    print("Maximum arrival rate : < ", lambdaMax)

def main():
    print("Simulation started at: ", datetime.datetime.now())
    print("Starting simultation for exercise 1...")
    print("Intializing event queue, server and random number generator...")
    
    eventQueue = EventQueue()
    rng = randomGenerator()
    server = Server()
    currentTime = 0.0
    waitingQueue = []
    totalTimeSpent = []

    exponential = round(rng.generateExponentialRandNum(lam), 4)
    print("Exponential number generated: ", exponential)

    firstEvent = Event("ARRIVAL", exponential)
    eventQueue.addEventbasedOnTimestamp(firstEvent)
    print("First event added to the queue with timestamp: ", exponential)

    MAX = 1048576

    while not eventQueue.isEmpty():
        currentEvent = eventQueue.removeEvent()
        currentTime = currentEvent.timestamp
        
        if currentTime > MAX:
            break

        if currentEvent.eventType == "ARRIVAL":
            arrivalEx1(currentEvent, currentTime, eventQueue, server, rng, waitingQueue)
        
        elif currentEvent.eventType == "DEPARTURE":
            departureEx1(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, mu)

    
    print("Simulation ended at: ", datetime.datetime.now())
    print("Calculating confidence interval and plotting results...")
    
    plot(totalTimeSpent, confidenceInterval(totalTimeSpent), True)

    print("Simulation completed successfully for exercise 1!")
    print("Starting simultation for exercise 2...")
    print("Resetting event queue, server, waiting queue and total time spent...")
    
    eventQueue = EventQueue()
    rng = randomGenerator()
    server = Server()
    currentTime = 0.0
    waitingQueue = []
    totalTimeSpent = []

    print("Finding max value in x...")

    X = np.linspace(0, 6, MAX)
    M = max(newServiceTime(x) for x in X)

    print("Found maximum height M: ", M)

    getAvgServiceTime(M, rng)
    exponential = round(rng.generateExponentialRandNum(lam2), 4)
    
    print("Exponential number generated: ", exponential)

    firstEvent = Event("ARRIVAL", exponential)
    eventQueue.addEventbasedOnTimestamp(firstEvent)
    
    print("First event added to the queue with timestamp: ", exponential)

    while not eventQueue.isEmpty():
        currentEvent = eventQueue.removeEvent()
        currentTime = currentEvent.timestamp
        
        if currentTime > MAX:
            break

        if currentEvent.eventType == "ARRIVAL":
            arrivalEx2(currentEvent, currentTime, eventQueue, server, rng, waitingQueue, M)
        
        elif currentEvent.eventType == "DEPARTURE":
            departureEx2(currentTime, eventQueue, server, rng, waitingQueue, totalTimeSpent, M)

    print("Simulation ended at: ", datetime.datetime.now())
    print("Calculating confidence interval and plotting results...")
    
    plot(totalTimeSpent, confidenceInterval(totalTimeSpent), False)

    return 0


if __name__ == "__main__":
    main()