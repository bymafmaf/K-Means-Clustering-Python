import csv
import sys
import math
import random
import matplotlib.pyplot as plt
import numpy

class Cluster(object):
    def __init__(self, centroid):
        self.centroid = centroid
        self.members = []

    def addEntry(self, entry):
        self.members.append(entry)
    def changeCentroid(self, centroid):
        self.centroid = centroid
    def getWCScore(self, isManhattan):
        score = 0
        for entry in self.members:
            dist = distance(self.centroid, entry, isManhattan)
            dist = math.pow(dist, 2)
            score += dist
        return score

def loadCsv(filename): # we eliminate all unnecessary attributes
    lines = csv.reader(open(filename, "rb"))
    next(lines, None)
    dataset = list(lines)
    entryLength = len(dataset[0])
    for i in range(len(dataset)):
        attrNum = 0
        while (attrNum < entryLength):
            if (attrNum < 3):
                dataset[i].pop(0)
            elif (attrNum == 5):
                dataset[i].pop(2)
            elif (attrNum > 7):
                dataset[i].pop(4)
            attrNum += 1
        for index, val in enumerate(dataset[i]):
            dataset[i][index] = float(val)
    return dataset

def distance(first, second, isManhattan):
    result = 0
    if isManhattan:
        for index, val in enumerate(first):
            result += val - second[index]
    else:
        sum = 0
        for index, val in enumerate(first):
            sum += math.pow(val-second[index], 2)
        result = math.sqrt(sum)
    return result

def generateRandomCentroids(dataset, k):
    points = random.sample(dataset, k)
    clusters = []
    for centroid in points:
        cluster = Cluster(centroid)
        clusters.append(cluster)
    return clusters
def connectToClusters(dataset, clusters, isManhattan):
    for entry in dataset:
        minDistance = 9999999.99
        resultCentroidIndex = 0
        for index, cluster in enumerate(clusters):
            dist = distance(cluster.centroid, entry, isManhattan)
            if ( dist < minDistance ):
                minDistance = dist
                resultCentroidIndex = index
        clusters[resultCentroidIndex].addEntry(entry)
def changeClustersWithData(clusters):
    for idx, cluster in enumerate(clusters):
        newMeanCentroid = [0, 0, 0, 0]
        for entry in cluster.members:
            for index, val in enumerate(entry):
                newMeanCentroid[index] += val/len(cluster.members)
        clusters[idx].changeCentroid(newMeanCentroid)
def changeMembersWithNewClusters(clusters, isManhattan):
    numOfChanges = 0
    for mainIndex, mainCluster in enumerate(clusters):
        for entry in mainCluster.members:
            currentDistance = distance(mainCluster.centroid, entry, isManhattan)
            minDistance = currentDistance
            resultClusterIndex = mainIndex
            for subIndex, subCluster in enumerate(clusters):
                dist = distance(subCluster.centroid, entry, isManhattan)
                if dist < minDistance:
                    minDistance = dist
                    resultClusterIndex = subIndex
            if resultClusterIndex != mainIndex:
                mainCluster.members.remove(entry)
                clusters[resultClusterIndex].members.append(entry)
                numOfChanges += 1
    return numOfChanges
def loggedLoadCsv(filename): # we eliminate all unnecessary attributes
    lines = csv.reader(open(filename, "rb"))
    next(lines, None)
    dataset = list(lines)
    entryLength = len(dataset[0])
    for i in range(len(dataset)):
        attrNum = 0
        while (attrNum < entryLength):
            if (attrNum < 3):
                dataset[i].pop(0)
            elif (attrNum == 5):
                dataset[i].pop(2)
            elif (attrNum > 7):
                dataset[i].pop(4)
            attrNum += 1
        for index, val in enumerate(dataset[i]):
            if index == 2 | index == 3:
                dataset[i][index] = math.log(float(val))
            else:
                dataset[i][index] = float(val)
    return dataset
def standardizedLoadCsv(filename): # we eliminate all unnecessary attributes
    lines = csv.reader(open(filename, "rb"))
    next(lines, None)
    dataset = list(lines)
    entryLength = len(dataset[0])
    for i in range(len(dataset)):
        attrNum = 0
        while (attrNum < entryLength):
            if (attrNum < 3):
                dataset[i].pop(0)
            elif (attrNum == 5):
                dataset[i].pop(2)
            elif (attrNum > 7):
                dataset[i].pop(4)
            attrNum += 1
        for index, val in enumerate(dataset[i]):
            dataset[i][index] = float(val)
    meanSet = []
    stdSet = []
    totalArray = {0:[],1:[],2:[],3:[]}
    for entry in dataset:
        for index,attrVal in enumerate(entry):
            totalArray[index].append(attrVal)
    for index,attr in enumerate(totalArray):
        meanSet.append(numpy.mean(totalArray[index]))
        stdSet.append(numpy.std(totalArray[index]))
    for index, entry in enumerate(dataset):
        for aIndex, attrVal in enumerate(dataset[index]):
            dataset[index][aIndex] = abs( (dataset[index][aIndex]-meanSet[aIndex])/stdSet[aIndex] )
    return dataset

def plotLat(clusters, isReview):
    for oneCluster in clusters:
        colorNum = numpy.random.rand(3,1)
        if isReview:
            plt.scatter(oneCluster.centroid[2], oneCluster.centroid[3], marker = "x", c=colorNum, s=100)
        else:
            plt.scatter(oneCluster.centroid[0], oneCluster.centroid[1], marker="x", c=colorNum, s=100)
        xValues = []
        yValues = []
        for entry in oneCluster.members:
            if isReview:
                xValues.append(entry[2])
                yValues.append(entry[3])
            else:
                xValues.append(entry[0])
                yValues.append(entry[1])
        plt.scatter(xValues, yValues, marker="o", c=colorNum, s=25)
    if isReview:
        plt.xlabel("Review Count")
        plt.ylabel("Checkins")
    else:
        plt.xlabel("Lattitude")
        plt.ylabel("Logntitude")
    plt.show()

def main():
    kNumber = int(sys.argv[2])
    clusteringOption = int(sys.argv[3])
    plotOption = sys.argv[4]

    if clusteringOption == 2:
        dataset = loggedLoadCsv(sys.argv[1])
    elif clusteringOption == 3:
        dataset = standardizedLoadCsv(sys.argv[1])
    else:
        dataset = loadCsv(sys.argv[1]) #argv1
    clusters = generateRandomCentroids(dataset, kNumber)
    if clusteringOption == 1:
        isManhattan = False
        connectToClusters(dataset, clusters, isManhattan)

        changeClustersWithData(clusters)
        while changeMembersWithNewClusters(clusters, isManhattan) != 0:
            changeClustersWithData(clusters)

        totalScore = 0
        for index, cluster in enumerate(clusters):
            totalScore += cluster.getWCScore(isManhattan)
        print "WC-SSE=" + str(totalScore)

        for index, cluster in enumerate(clusters):
            print "Centroid" + str(index + 1) + "=" + str(cluster.centroid)
    elif clusteringOption == 4:
        isManhattan = True
        connectToClusters(dataset, clusters, isManhattan)

        changeClustersWithData(clusters)
        while changeMembersWithNewClusters(clusters, isManhattan) != 0:
            changeClustersWithData(clusters)

        totalScore = 0
        for index, cluster in enumerate(clusters):
            totalScore += cluster.getWCScore(isManhattan)
        print "WC-SSE=" + str(totalScore)

        for index, cluster in enumerate(clusters):
            print "Centroid" + str(index + 1) + "=" + str(cluster.centroid)
    elif clusteringOption == 5:
        percentNum = int(len(dataset) * 0.01)
        downSampled = random.sample(dataset, percentNum)

        clusters = generateRandomCentroids(downSampled, kNumber)
        isManhattan = False
        connectToClusters(downSampled, clusters, isManhattan)

        changeClustersWithData(clusters)
        while changeMembersWithNewClusters(clusters, isManhattan) != 0:
            changeClustersWithData(clusters)

        totalScore = 0
        for index, cluster in enumerate(clusters):
            totalScore += cluster.getWCScore(isManhattan)
        print "WC-SSE=" + str(totalScore)

        for index, cluster in enumerate(clusters):
            print "Centroid" + str(index + 1) + "=" + str(cluster.centroid)



    if plotOption == "1":
        plotLat(clusters, False)
    if plotOption == "2":
        plotLat(clusters, True)

main()

