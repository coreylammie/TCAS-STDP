# -----------------------------------------------------------------------------------------------------------------------------------
# Encodes the triplet-based experiments as a temporally encoded spike train
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np


# Method to encode the triplet experiments
def encodeTripletExperiment(deltaT1, deltaT2):
    # Determine the total length required
    totalLengthRequired = abs(deltaT1) + abs(deltaT2) + 1
    # Initialize the spike train
    spikeTrain = np.zeros((2,totalLengthRequired))
    if (deltaT2 < 0):
        spikeTrain[0,0] = 1
        spikeTrain[0,-1] = 1
        spikeTrain[1,abs(deltaT1)] = 1
    if (deltaT1 < 0):
        spikeTrain[1, 0] = 1
        spikeTrain[1, -1] = 1
        spikeTrain[0, abs(deltaT1)] = 1

    return np.array(spikeTrain)

deltaT1 = 5
deltaT2 = -5
res = encodeTripletExperiment(deltaT1, deltaT2)
