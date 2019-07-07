# -----------------------------------------------------------------------------------------------------------------------------------
# Approximates decimal values with 2^N values
# -----------------------------------------------------------------------------------------------------------------------------------
# Imports
import math


# Method to approximate a given decimal value
def approxDecimal(inputDecimalValue):
    k = math.log2(inputDecimalValue)
    print('---------------------------------------------------------')
    print('2^[%f] = %f' % (k, inputDecimalValue))
    roundUp = math.ceil(k)
    roundDown = math.floor(k)
    upperValue = 2**roundUp
    lowerValue = 2**roundDown
    dif1 = abs(inputDecimalValue - upperValue)
    dif2 = abs(inputDecimalValue - lowerValue)
    if (dif1 < dif2):
        perc = (dif1/inputDecimalValue)*100
        res = roundUp
    else:
        perc = (dif2/inputDecimalValue)*100
        res = roundDown
    print('%f Approximately Equal to 2^[%i] = %f' % (inputDecimalValue, res, 2**res))
    print('Percentage Error of: %f' % perc)

approxDecimal(0.00299072)
