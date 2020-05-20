import numpy as np
import pandas as pd
import matplotlib as plt
import math

from Reg import Reg

# xList:np.ndarray = np.array([0.7, 0.96, 1.13, 1.57, 1.92])
# yList:np.ndarray = np.array([0.19, 0.21, 0.23, 0.25, 0.31])

xList:np.ndarray = np.array([80, 40, -40, -120, -200, -280])
yList:np.ndarray = np.array([6.47, 6.24, 5.72, 5.09, 4.30, 3.33])

linReg = Reg()
linReg.insertList(xList, yList)

linReg.getPolConstant()
