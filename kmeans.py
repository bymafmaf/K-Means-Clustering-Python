import csv
import sys
import math
import numpy
import random

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


def main():
    dataset = loadCsv(sys.argv[1]) #argv1
    kNumber = int(sys.argv[2])
    clusteringOption = int(sys.argv[3])
    plotOption = sys.argv[4]
    clusters = generateRandomCentroids(dataset, kNumber)
    isManhattan = False
    connectToClusters(dataset, clusters, isManhattan)

    loopNum = 0
    changeClustersWithData(clusters)
    while changeMembersWithNewClusters(clusters, isManhattan) != 0:
        changeClustersWithData(clusters)
        loopNum+=1
        print "loop num: " + str(loopNum)

    totalScore = 0
    for index, cluster in enumerate(clusters):
        print "Centroid" + str(index+1) + "=" + str(cluster.centroid)
        totalScore += cluster.getWCScore(isManhattan)
    print "WC Score: " + str(totalScore)


main()

