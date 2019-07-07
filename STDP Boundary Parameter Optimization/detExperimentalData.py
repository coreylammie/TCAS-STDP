# -----------------------------------------------------------------------------------------------------------------------------------
# Determines the NMSE of the enumalted digital model with regards to the experimental data
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from numpy import interp
from random import randint
import cv2
import math
from GenSpikeTrain import GenSpikeTrain
from genDE import genDE
from synapse import Synapse
from matplotlib import pyplot as plt
from encodeTripletExperiment import *
from encodePairExperiment import *
from encodeQuadExperiment import *


# Method to determine the epxerimental data
def detExperimentalData(inputArr):
    # Initialize the result array
    res = np.zeros(13)
    print('---------------------------------------------------------')
    # Pair-Based Dataset
    res[0] = detTotalWeightChange(inputArr, encodePairExperiment(10), 60, False)
    print('Pair Based Experiment    [10]: %f' % res[0])
    res[1] = detTotalWeightChange(inputArr, encodePairExperiment(-10), 60, False)
    print('Pair Based Experiment    [-10]: %f' % res[1])
    print('')
    # Triplet-Based Dataset
    res[2] = detTotalWeightChange(inputArr, encodeTripletExperiment(5, -5), 60, False)
    print('Triplet Based Experiment [5, -5]: %f' % res[2])
    res[3] = detTotalWeightChange(inputArr, encodeTripletExperiment(10, -10), 60, False)
    print('Triplet Based Experiment [10, -10]: %f' % res[3])
    res[4] = detTotalWeightChange(inputArr, encodeTripletExperiment(15, -5), 60, False)
    print('Triplet Based Experiment [15, -5]: %f' % res[4])
    res[5] = detTotalWeightChange(inputArr, encodeTripletExperiment(5, -15), 60, False)
    print('Triplet Based Experiment [5, -15]: %f' % res[5])
    res[6] = detTotalWeightChange(inputArr, encodeTripletExperiment(-5, 5), 60, False)
    print('Triplet Based Experiment [-5, 5]: %f' % res[6])
    res[7] = detTotalWeightChange(inputArr, encodeTripletExperiment(-10, 10), 60, False)
    print('Triplet Based Experiment [-10, 10]: %f' % res[7])
    res[8] = detTotalWeightChange(inputArr, encodeTripletExperiment(-5, 15), 60, False)
    print('Triplet Based Experiment [-5, 15]: %f' % res[8])
    res[9] = detTotalWeightChange(inputArr, encodeTripletExperiment(-15, 5), 60, False)
    print('Triplet Based Experiment [-15, 5]: %f' % res[9])
    print('')
    # Quadruplet-Based Dataset
    res[10] = detTotalWeightChange(inputArr, encodeQuadExperiment(-89, 5), 60, False)
    print('Quadruplet Based Experiment    [-89, 5]: %f' % res[10])
    res[11] = detTotalWeightChange(inputArr, encodeQuadExperiment(84, 5), 60, False)
    print('Quadruplet Based Experiment    [84, 5]: %f' % res[11])
    res[12] = detTotalWeightChange(inputArr, encodeQuadExperiment(20, 5), 60, False)
    print('Quadruplet Based Experiment    [20, 5]: %f' % res[12])
    print('---------------------------------------------------------')
    return res


# Method to determine the total weight change
def detTotalWeightChange(inputArr, spikeTrain, iterations, showPlot):
    # Initialize the time steps required to emulate the total runtime iteratively
    dt = 1  # Time between iterations
    train = spikeTrain
    totalDuration = train.shape[1]  # Total duration to run
    timeToEnumerate = np.arange(1, totalDuration + 1, 1)  # Determine the time-step array [0, 0.125, 0.25, 0.375, ..., 800]
    # Assign initial parameters
    # ---------------------------------
    tauX = 512
    tauY = 64
    tauPlus = 16
    tauMinus = 32
    # ---------------------------------
    A2Plus = inputArr[0]
    A2Minus = inputArr[1]
    A3Plus = inputArr[2]
    A3Minus = inputArr[3]
    # ---------------------------------
    r1 = genDE(tauPlus, True, dt)
    r2 = genDE(tauX, True, dt)
    o1 = genDE(tauMinus, False, dt)
    o2 = genDE(tauY, False, dt)
    # ---------------------------------
    syn = Synapse(0, A2Plus, A2Minus, A3Plus, A3Minus)
    synWeight = np.zeros((1, math.floor(totalDuration / dt)))
    # Enumerate through the total runtime
    for timeIndex, currentTime in enumerate(timeToEnumerate):
        # Update the current state of t-pre and t-post
        tpre = (train[0, timeIndex] == 1)
        tpost = (train[1, timeIndex] == 1)
        # Update the current values of r1, r2, o1 and o2
        r1.updateSynapticWeight(tpre, tpost)
        r2.updateSynapticWeight(tpre, tpost)
        o1.updateSynapticWeight(tpre, tpost)
        o2.updateSynapticWeight(tpre, tpost)
        # Update the current synaptic weight
        syn.updateSynapticWeight(tpre, tpost, r1.currentValue, r2.currentValue, o1.currentValue, o2.currentValue)
        currentVal = syn.currentWeight
        # print(currentVal) #For Debugging
        synWeight[0, timeIndex] = currentVal
    totalWeightChange = synWeight[0, -1] - synWeight[0, 0]
    if (showPlot):
        print('Total Weight Change: [%f]' % (totalWeightChange))
        print('Total Weight Change [n = 60]: [%f]' % (totalWeightChange * 60))
        plt.plot(timeToEnumerate, synWeight[0, :], label='Change in Synaptic Weight')
        plt.legend(loc='lower center')
        plt.title('Change in Synaptic Weight')
        plt.xlim([0, totalDuration])
        plt.show()
    return totalWeightChange * iterations


def detNMSE(experimentalData, experimentalStDev, calculatedData):
    if (len(experimentalData) == len(experimentalStDev) == len(calculatedData)):
        currentNMSE = 0
        for i in range(len(experimentalData)):
            currentNMSE += (abs(experimentalData[i] - calculatedData[i])**2)/(experimentalStDev[i]**2)
        currentNMSE = currentNMSE/len(experimentalData)
        return currentNMSE
    else:
        print('detNMSE: Mismatched Size!')
        exit()

A2Plus = 4.6 * 10 ** (-3)
A2Minus = 3 * 10 ** (-3)
A3Plus = 9.1 * 10 ** (-3)
A3Minus = 7.5 * 10 ** (-9)
inputArr = [A2Plus, A2Minus, A3Plus, A3Minus]

calculatedData = detExperimentalData(inputArr)
experimentalData = [0.25, -0.17, -0.01, 0.03, 0.01, 0.24, 0.33, 0.34, 0.22, 0.29, -0.003, 0.06, 0.21]
experimentalStDev = [0.05, 0.05, 0.04, 0.04, 0.03, 0.06, 0.04, 0.04, 0.08, 0.05, 0.03, 0.04, 0.04]

NMSE = detNMSE(experimentalData, experimentalStDev, calculatedData)
print('NMSE = [%f]' % NMSE)
