
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import math

from LinReg import LinReg
from PolReg import PolReg
from ExpReg import ExpReg
from InOut import InOut

def plot(xList:np.ndarray, yList:np.ndarray, linRegList:np.ndarray, expRegList:np.ndarray, polRegDict:dict):
    if (xList.size < 2):
        return -1

    fig, ax = plt.subplots(figsize = (20,15))
    df = pd.DataFrame()

    df["x (Sample Data)"] = xList
    xList:np.ndarray = xList.astype(float)

    ax.set_title("Regression Comparison Graph")

    if (xList.size == yList.size):
        ax.scatter(xList, yList.astype(float),
                   label = "Sample Data",
                   marker = "o",
                   s = 30,
                   c = "red",
                   alpha = 0.8,
                   zorder =1)
        df["y (Sample Data)"] = yList

    if (xList.size == linRegList.size):
        ax.plot(xList, linRegList.astype(float),
                label = f"Linear",
                marker = "x",
                markersize = 10,
                zorder = 0.5)
        df["Linear Regression"] = linRegList
        
    if (xList.size == expRegList.size):
        ax.plot(xList, expRegList.astype(float),
                label = f"Exponential",
                marker = "x",
                markersize = 10,
                zorder = 0.5)
        df["Exponential Regression"] = expRegList

    for key in polRegDict:
        if (xList.size == polRegDict[key].size):
            ax.plot(xList, polRegDict[key].astype(float),
                    label = f"Order {key}",
                    marker = "x",
                    markersize = 10,
                    zorder = 0.5)
            df[f"Polynomial Order {key}"] = polRegDict[key]

    ax.legend(title = "Legend",
              fontsize = "large")

    plt.show()
    print(df)


def main():
    isDataFilled:bool = False

    linReg:LinReg = LinReg()
    expReg:ExpReg = ExpReg()
    polReg:PolReg = PolReg()

    while (True):
        option:int = 0

        print("=== Main Menu ===")
        print("[1] Add Data\n[2] Plot\n[3] Find Best Fit\n[0] Exit")
        option = input("Please input option: ")
        
        if (option == "1"):
            while (True):
                print("=== Add Data ===")
                print("[1] Add Manually\n[2] Add from existing CSV file\n[9] Back\n[0] Exit")
                option = input("Please input option: ")

                if (option == "1"):
                    coordList:list = []
                    while (True):
                        value:str = ""
                        
                        print("=== Add Data Manually ===")
                        print(coordList)
                        print("done | cancel")
                        value = input("Input value [x,y]:")

                        if (value == "done"):
                            linReg.insertList(np.array(coordList))
                            expReg.insertList(np.array(coordList))
                            polReg.insertList(np.array(coordList))
                            isDataFilled = True
                            break
                        elif (value == "cancel"):
                            break
                        else:
                            try:
                                tempCoord:np.array = np.array(value.split(",")).astype(float)
                                if (tempCoord.size == 2):
                                    coordList.append(tempCoord)
                                else:
                                    raise NameError("Invalid input!") 
                            except:
                                print("Invalid input!")

                elif (option == "2"):
                    inOut:InOut = InOut()
                    xList:np.ndarray = np.array([])
                    yList:np.ndarray = np.array([])

                    while (True):
                        fileName:str = ""
                        fileName = input ("Please input file name (path): ")
                        xList, yList = inOut.read(fileName)

                        if (xList.size != 0 and yList.size != 0):
                            linReg.insertList(xList, yList)
                            expReg.insertList(xList, yList)
                            polReg.insertList(xList, yList)
                            isDataFilled = True
                            break
                        else:
                            option = input("Try again? [y/n]: ")
                            if (option == "y"):
                                pass
                            elif (option == "n"):
                                break
                            else:
                                print("Invalid option!")

                elif (option == "9"):
                    break
                elif (option == "0"):
                    return
                else:
                    print("Invalid option!")

        elif (option == "2"):
            if (not isDataFilled):
                print("Data is empty!")
                continue
        elif (option == "3"):
            if (not isDataFilled):
                print("Data is empty!")
                continue
        elif (option == "0"):
            return
        else:
            print("Invalid option!")

# xList:np.ndarray = np.array([0.7, 0.96, 1.13, 1.57, 1.92])
# yList:np.ndarray = np.array([0.19, 0.21, 0.23, 0.25, 0.31])

# xList:np.ndarray = np.array([80, 40, -40, -120, -200, -280])
# yList:np.ndarray = np.array([6.47, 6.24, 5.72, 5.09, 4.30, 3.33])

# coordList:np.ndarray = np.array([[80,6.47], [40,6.24], [-40,5.72], [-120,5.09], [-200, 4.30], [-280, 3.33]])
# coordList:np.ndarray = np.array([[1, 0.891], [3,0.708], [5, 0.562], [7, 0.447], [9, 0.355]])

x = np.array([0,1,2])
y = np.array([50,100,150])
# coord = np.array([[1,2],[3,4]])
# a = LinReg()
# b = ExpReg()
c = PolReg()

c.insertList(x,y,3)
print(c.getCoeff())

# a.insertList(coordList)
# b.insertList(coordList)

# print(a.getCoeff())
# print(b.getCoeff())

# print()

# print(a.getReg())
# print(b.getReg())

# print()

# print(a.getStdError())
# print(b.getStdError())

# print()

# print(a.getSize())
# print(b.getSize())