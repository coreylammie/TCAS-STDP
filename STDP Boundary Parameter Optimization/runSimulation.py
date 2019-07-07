# -----------------------------------------------------------------------------------------------------------------------------------
# Run the simulation for a randomly generated spike train
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

#import scipy.optimize

def runSimulation(inputArr):
    # Initialize the time steps required to emulate the total runtime iteratively
    totalDuration = 1000  # Total duration to run
    dt = 1  # Time between iterations
    timeToEnumerate = np.arange(1, totalDuration + 1, 1)  # Determine the time-step array [0, 0.125, 0.25, 0.375, ..., 800]

    # Generate a random pre-synaptic and post-synaptic spike train to send to the network
    trainGen = GenSpikeTrain(math.floor(totalDuration/dt))
    preTrain = trainGen.SpikeTrainGen()
    postTrain = trainGen.SpikeTrainGen()
    train = np.vstack((preTrain, postTrain))

    # Assign initial parameters
    # ---------------------------------
    tauX = 575
    tauY = 47
    tauPlus = 16.8
    tauMinus = 33.7
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
    # ---------------------------------
    synWeight = np.zeros(math.floor(totalDuration/dt))

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
        synWeight[timeIndex] = currentVal

    totalWeightChange = synWeight[-1] - synWeight[0]
    print('Total Weight Change: [%f]' % (totalWeightChange))
    plt.plot(timeToEnumerate, synWeight)
    plt.title('Change in Synaptic Weight for Random Spike Train Inputs')
    plt.xlim([0,500])
    plt.show()

A2Plus = 0.00022902
A2Minus = 0.0006855
A3Plus = 0.00635653
A3Minus = 0.00134848
inputArr = [A2Plus, A2Minus, A3Plus, A3Minus]
runSimulation(inputArr)
