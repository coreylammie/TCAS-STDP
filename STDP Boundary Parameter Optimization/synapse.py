# -----------------------------------------------------------------------------------------------------------------------------------
# Class to govern the behaviour of the implimented synapses
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from numpy import interp
from random import randint
import cv2
import math


class Synapse:

    # Class Constructor
    def __init__(self, initialWeight, A2Plus, A2Minus, A3Plus, A3Minus):
        self.currentWeight = initialWeight
        self.A2Plus = A2Plus
        self.A2Minus = A2Minus
        self.A3Plus = A3Plus
        self.A3Minus = A3Minus

    # Method to update the synaptic weight
    def updateSynapticWeight(self, tpre, tpost, r1val, r2val, o1val, o2val):
        if (tpre):
            #self.currentWeight -= o1val*(self.A2Minus + self.A3Minus*r2val) -- PSTDP
            self.currentWeight -= o1val*self.A2Minus + self.fourBitApproximation(o1val, r2val)*self.A3Minus
        if (tpost):
            #self.currentWeight += r1val*(self.A2Plus + self.A3Plus*o2val) -- PSTDP
            self.currentWeight += r1val*self.A2Plus + self.fourBitApproximation(r1val, o2val)*self.A3Plus

    # Method to determine the four bit quantized approximation
    def fourBitApproximation(self, inputA, inputB):
        if (inputA == 1):
            return inputB
        elif (inputB == 1):
            return inputA
        elif (inputA == 0 or inputB == 0):
            return 0
        else:
            inputATrunc = round(inputA/(2**(-4)))
            inputBTrunc = round(inputB/(2**(-4)))
            return inputATrunc*inputBTrunc*(2**(-8))
