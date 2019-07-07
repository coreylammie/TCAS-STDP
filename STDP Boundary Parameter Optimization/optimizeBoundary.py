# -----------------------------------------------------------------------------------------------------------------------------------
# Script used in order to optimize the boundary conditions of the differential equations governing the behaviour of the network
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from numpy import interp
from random import randint
import cv2
import math
from genDE import genDE
from synapse import Synapse
from matplotlib import pyplot as plt
from encodeTripletExperiment import *
from encodePairExperiment import *
from encodeQuadExperiment import *
import scipy.optimize


# Method to determine the experimental data
def detExperimentalData(inputArr):
    res = np.zeros(161)
    print('---------------------------------------------------------')
    # Pair-based Dataset
    k = np.linspace(-80,80,161)
    for i,val in enumerate(k):
        res[i] = detTotalWeightChange(inputArr, encodePairExperiment(int(k[i])), 60, False)
        print('%f, ' % res[i],end='')
    return res


# Method to ddetermine the total weight change
def detTotalWeightChange(inputArr, spikeTrain, iterations, showPlot):
    # Initialize the time steps required to emulate the total runtime iteratively
    dt = 1  # Time between iterations
    train = spikeTrain
    totalDuration = train.shape[1]  # Total duration to run
    timeToEnumerate = np.arange(1, totalDuration + 1, 1)  # Determine the time-step array [0, 0.125, 0.25, 0.375, ..., 800]
    # Assign initial parameters
    # ---------------------------------
    tauX = 1024
    tauY = 32
    tauPlus = 64
    tauMinus = 256
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
        syn.updateSynapticWeight(tpre, tpost, r1.currentValue, r2.previousValue, o1.currentValue, o2.previousValue)
        currentVal = syn.currentWeight
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


# Method to determine the NMSE
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


# Function to optimize
def functionToOptimize():
    inputArr = [2**(-8), 2**(-9), 2**(-8), 2**(-10)]
    calculatedData = detExperimentalData(inputArr)
    experimentalData = [0.25, -0.17, -0.01, 0.03, 0.01, 0.24, 0.33, 0.34, 0.22, 0.29, -0.003, 0.06, 0.21]
    experimentalStDev = [0.05, 0.05, 0.04, 0.04, 0.03, 0.06, 0.04, 0.04, 0.08, 0.05, 0.03, 0.04, 0.04]
    NMSE = detNMSE(experimentalData, experimentalStDev, calculatedData)

    # A2Plus = 4.6 * 10 ** (-3)
    # A2Minus = 3 * 10 ** (-3)
    # A3Plus = 9.1 * 10 ** (-3)
    # A3Minus = 7.5 * 10 ** (-9)
    # inputArr = [A2Plus, A2Minus, A3Plus, A3Minus]

    print('NMSE = [%f]' % NMSE);
    return NMSE

#inputopt = scipy.optimize.fmin(functionToOptimize, [1])
inputopt = functionToOptimize()
print(inputopt)
