# -----------------------------------------------------------------------------------------------------------------------------------
# Generates the required diffirential equations to model the synapse dynamics
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from numpy import interp
from random import randint
import cv2
import math


class genDE:

    # Class Constructor
    def __init__(self, tauConstant, incrimentOnPre, deltaT):
        self.tauConstant = tauConstant
        self.tpre = 0
        self.tpost = 0
        self.deltaT = deltaT
        self.currentValue = 0
        self.deltaValue = 0
        self.incrimentOnPre = incrimentOnPre
        self.previousValue = 0

    # Method to update the synaptic weight
    def updateSynapticWeight(self, tpre, tpost):
        self.previousValue = self.currentValue
        self.tpre = tpre
        self.tpost = tpost
        if (self.incrimentOnPre and self.tpre):
            self.deltaValue = 1
        elif (not (self.incrimentOnPre) and self.tpost):
            self.deltaValue = 1
        else:
            self.deltaValue = -self.currentValue / self.tauConstant
        self.currentValue += self.deltaValue*self.deltaT
