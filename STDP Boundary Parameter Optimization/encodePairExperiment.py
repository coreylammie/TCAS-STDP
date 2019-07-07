# -----------------------------------------------------------------------------------------------------------------------------------
# Encodes the pair-based experiments as a temporally encoded spike train
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np


# Method to encode the paired-based experiments
def encodePairExperiment(deltaT):
    # Determine the total length required
    totalLengthRequired = abs(deltaT) + 1
    # Initialize the spike train
    spikeTrain = np.zeros((2,totalLengthRequired))
    if (deltaT > 0):
        spikeTrain[0, 0] = 1
        spikeTrain[1, -1] = 1
    else:
        spikeTrain[1, 0] = 1
        spikeTrain[0, -1] = 1

    return np.array(spikeTrain)

deltaT = -10
res = encodePairExperiment(deltaT)
print(res.shape[1])
