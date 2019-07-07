# -----------------------------------------------------------------------------------------------------------------------------------
# Encodes the quadruplet-based experiments as a temporally encoded spike train
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np

# Method to encode the quadruplet experiments
def encodeQuadExperiment(T, deltaT):
    # Determine the total length required
    totalLengthRequired = abs(T) + 2*abs(deltaT) + 1
    # Initialize the spike train
    spikeTrain = np.zeros((2,totalLengthRequired))
    if (T > 0):
        spikeTrain[1, 0] = 1
        spikeTrain[1, -1] = 1
        spikeTrain[0, deltaT] = 1
        spikeTrain[0, -deltaT-1] = 1
    else:
        spikeTrain[0, 0] = 1
        spikeTrain[0, -1] = 1
        spikeTrain[1, abs(deltaT)] = 1
        spikeTrain[1, -abs(deltaT) - 1] = 1

    return np.array(spikeTrain)

T = -20
deltaT = 5
res = encodeQuadExperiment(T, deltaT)
print(res.shape[1])
