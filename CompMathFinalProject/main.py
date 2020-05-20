import numpy as np
import pandas as pd
import matplotlib as plt
import math

from LinReg import LinReg

xList:np.ndarray = np.array([0.7, 0.96, 1.13, 1.57, 1.92])
yList:np.ndarray = np.array([0.19, 0.21, 0.23, 0.25, 0.31])

linReg = LinReg()
linReg.insertList(xList, yList)

linReg.getPolConstant()
print(linReg.getLinGradient())
print(linReg.getLinConstant())
