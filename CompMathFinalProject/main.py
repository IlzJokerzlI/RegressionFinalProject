import numpy as np
import pandas as pd
import matplotlib as plt
import math

from Reg import Reg

# xList:np.ndarray = np.array([0.7, 0.96, 1.13, 1.57, 1.92])
# yList:np.ndarray = np.array([0.19, 0.21, 0.23, 0.25, 0.31])

# xList:np.ndarray = np.array([80, 40, -40, -120, -200, -280])
# yList:np.ndarray = np.array([6.47, 6.24, 5.72, 5.09, 4.30, 3.33])

# coordList:np.ndarray = np.array([[80,6.47], [40,6.24], [-40,5.72], [-120,5.09], [-200, 4.30], [-280, 3.33]])

xList:np.ndarray = np.array([0,1,3,5,7,9])
yList:np.ndarray = np.array([1,0.891,0.708,0.562,0.447,0.355])

reg = Reg()
reg.insertList(xList, yList)

print(reg.getXList())
print("")
print(reg.getYList())
print("")
print(reg.getLinYReg())
print("")
print(reg.getPolYReg())
print("")
print(reg.getExpYReg())
print("")
