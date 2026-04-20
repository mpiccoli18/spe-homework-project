import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

lam = 1             #Lambda for exponential distribution
lam2 = 0.25         #Lambda for exercise 2: lam2 < lambdaMax
mu = 2              #Mu for exponential distribution

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

    def isEmpty(self):
        return self.front is None
    
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


def confidenceInterval(totalTimeSpent, batch=30000):
    data = totalTimeSpent[10000:]
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
    lowerBound = mean - marginOfError
    upperBound = mean + marginOfError
    print(f"Confidence Interval is between {lowerBound:.4f} and {upperBound:.4f}")
    return lowerBound, upperBound

def plot(totalTimeSpent, confidence, MaxArrival, isFirstEx):
    rate = 500
    averageRun = []
    sum = 0
    for i, time in enumerate(totalTimeSpent):
        sum += time
        if i % rate == 0:
            averageRun.append(sum / (i + 1))
    
    axisX = np.arange(0, len(totalTimeSpent), rate)
    #print(len(averageRun))
    fig, zoom = plt.subplots(figsize=(10, 6))
    plt.plot(axisX, averageRun, color='b', label="Running Average", linewidth=1.5)
    
    CI = confidence
    plt.fill_between(axisX, CI[0], CI[1], color='orange', alpha=0.3, label="Confidence Interval")

    zoomAxis = zoom.inset_axes([0.5, 0.2, 0.3, 0.2])
    zoomAxis.plot(axisX, averageRun, color='b', linewidth=1.5)
    zoomAxis.fill_between(axisX, CI[0], CI[1], color='orange', alpha=0.3)
    minZoom = len(totalTimeSpent) * 0.80
    maxZoom = len(totalTimeSpent)
    zoomAxis.set_xlim(minZoom, maxZoom)
    minY = CI[0] - (CI[0] / 100)
    maxY = CI[1] + (CI[1] / 100)
    #print("Min: ", minY, " Max: ", maxY);
    zoomAxis.set_ylim(minY, maxY)
    zoomAxis.set_xticks([])
    zoomAxis.set_yticks([])
    zoom.indicate_inset_zoom(zoomAxis, edgecolor="black")

    if isFirstEx:
        average = 1 / (mu - lam)
        plt.axhline(y=average, color='r', linestyle='--', label="Theoretical Average", linewidth=2)
        zoomAxis.axhline(y=average, color='r', linestyle='--', linewidth=2)

    plt.xlim(None, len(totalTimeSpent))
    plt.ylim(0, max(averageRun) * 1.05)
    plt.xlabel("Number of Packets Processed", fontsize=12, labelpad=15)
    plt.ylabel("Average Time in System (s)", fontsize=12, labelpad=15)
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    plt.gca().tick_params(axis='both', which='both', labelsize=12)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="best", fontsize=10)

    if isFirstEx:
        plt.title("Exercise 1\n", fontsize=16, fontweight="bold", fontname="Arial", loc="center")
        plt.gca().text(0.5, 1.02, f"$\\lambda = {lam}, \\mu = {mu}$", fontsize=12, fontstyle="italic", ha="center", transform=plt.gca().transAxes)
        plt.savefig("Exercise1.pdf", format="pdf", bbox_inches="tight", transparent=False)
        print("Saved plot as Exercise1.pdf")
    else:
        plt.title("Exercise 2\n", fontsize=16, fontweight="bold", fontname="Arial", loc="center")
        plt.gca().text(0.5, 1.02, f"$\\lambda = {lam2} < \\lambda_{{Max}} = {MaxArrival:.4f}$", fontsize=12, fontstyle="italic", ha="center", transform=plt.gca().transAxes)
        plt.savefig("Exercise2.pdf", format="pdf", bbox_inches="tight", transparent=False)
        print("Saved plot as Exercise2.pdf")
    plt.show()


def newServiceTime(x):
    if x < 0 or x > 6:
        return 0
    elif x == 3:
        return 1.0
    else:
        return abs((math.sin(math.pi * (x - 3))) / (math.pi * (x - 3)))

def getAvgServiceTime(M, rng):
    totalNum = 1000000
    sum = 0
    for _ in range(totalNum):
        sum += rng.generateCustomServiceTime(M)
    
    avg = sum / totalNum
    lambdaMax = 1 / avg
    print(f"Estimated average service time: {avg:.4f}")
    print(f"Maximum arrival rate : < {lambdaMax:.4f}")
    return lambdaMax

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

    exponential = rng.generateExponentialRandNum(lam)
    print(f"Exponential number generated: {exponential:.4f}")

    firstEvent = Event("ARRIVAL", exponential)
    eventQueue.addEventbasedOnTimestamp(firstEvent)
    print("First event added to the queue with timestamp: ", exponential)

    MAX = 1000000
    M = 0
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
    
    plot(totalTimeSpent, confidenceInterval(totalTimeSpent), M, True)

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

    lambdaMax = getAvgServiceTime(M, rng)
    
    print(f"Exponential number generated: {exponential:.3f}")

    firstEvent = Event("ARRIVAL", exponential)
    eventQueue.addEventbasedOnTimestamp(firstEvent)
    
    print(f"First event added to the queue with timestamp: {exponential:.3f}")

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
    
    plot(totalTimeSpent, confidenceInterval(totalTimeSpent), lambdaMax, False)

    return 0


if __name__ == "__main__":
    main()