
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import math

from LinReg import LinReg
from PolReg import PolReg
from ExpReg import ExpReg
from InOut import InOut


# For plotting combination of all regression types
def plot(xList:np.ndarray, yList:np.ndarray, linRegList:np.ndarray, expRegList:np.ndarray, polRegDict:dict):
    if (xList.size < 2):
        return -1

    fig, ax = plt.subplots(figsize = (20,15))
    df = pd.DataFrame()

    df["x (Sample Data)"] = xList
    xList:np.ndarray = xList.astype(float)

    ax.set_title("Regression Comparison Graph")

    if (len(xList) == len(yList)):
        ax.scatter(xList, yList.astype(float),
                    label = "Sample Data",
                    marker = "o",
                    s = 30,
                    c = "red",
                    alpha = 0.8,
                    zorder =1)
        df["y (Sample Data)"] = yList

    if (len(xList) == len(linRegList)):
        ax.plot(xList, linRegList.astype(float),
                label = f"Linear",
                marker = "x",
                markersize = 10,
                zorder = 0.5)
        df["Linear Regression"] = linRegList
        
    if (len(xList) == len(expRegList)):
        ax.plot(xList, expRegList.astype(float),
                label = f"Exponential",
                marker = "x",
                markersize = 10,
                zorder = 0.5)
        df["Exponential Regression"] = expRegList

    for key in polRegDict:
        if (len(xList) == len(polRegDict[key])):
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


# Add Data Menu, expansion of Main Menu
def menuAddData(option:str, linReg:LinReg, expReg:ExpReg, polReg:PolReg):
    temp:np.ndarray = np.array([""])
    minOrder:int = 2 # Sets the min order to 2 (standard value)
    maxOrder:int = 2 # Sets the max order same as min order (standard value)


    if (option == "1" or option == "2" or option == "3"):
        while (True):
            print("\n\n=== Polynomial Order ===\n")
            try:
                print("[cancel]")
                temp:np.ndarray = np.array(input("Please input order of polynomial [min, max]: ").split(","))

                if (temp[0] == "cancel"):
                    return 2
                elif (len(temp) == 1 and temp[0] == ""):
                    break
                elif (len(temp) == 1):
                    temp = temp.astype(int)
                    minOrder = temp[0]
                    break
                elif (len(temp) == 2 and temp[0] == ""):
                    maxOrder = int(temp[1])
                    break
                elif (len(temp) == 2):
                    temp = temp.astype(int)
                    minOrder = temp[0]
                    maxOrder = temp[1]
                    break
                else:
                    print("\nINVALID INPUT!\n")
            except:
                print("\nINVALID INPUT!\n")


        # Add Data Manualy Menu
        if (option == "1"):
            coordList:list = []
            value:str = ""

            while (True):
                print("\n\n=== Add Data Manually ===\n")
                print(f"List: {coordList}\n")
                print("[done | cancel]")
                value = input("Input value [x,y]:")

                if (value == "done"):
                    linReg.insertList(np.array(coordList))
                    expReg.insertList(np.array(coordList))
                    polReg.insertList(np.array(coordList), minOrder = minOrder, maxOrder = maxOrder)
                    return 0
                elif (value == "cancel"):
                    return 2
                else:
                    try:
                        tempCoord:np.array = np.array(value.split(",")).astype(float)
                        if (tempCoord.size == 2):
                            coordList.append(tempCoord)
                        else:
                            raise NameError("INVALID INPUT!") 
                    except:
                        print("\nINVALID INPUT!\n")


        # Add Data From File Menu
        elif (option == "2" or "3"):
            inOut:InOut = InOut()
            xList:np.ndarray = np.array([])
            yList:np.ndarray = np.array([])

            while (True):
                print(("\n\n=== Add Data From File ===" if (option == "2") else "\n\n=== Add Data From Formated File ===\nNOTE: The csv file available is only for covid_19_data.csv because it is fixed. It can be changed inside InOut.py"))
                fileName:str = ""
                fileName = input ("Please input file name (path): ")
                if (option == "2"):
                    xList, yList = inOut.readStandard(fileName)
                elif (option == "3"):
                    xList, yList = inOut.readComplex(fileName)

                if (xList.size != 0 and yList.size != 0):
                    linReg.insertList(xList, yList)
                    expReg.insertList(xList, yList)
                    polReg.insertList(xList, yList, minOrder = minOrder, maxOrder = maxOrder)
                    return 0
                else:
                    while (True):
                        option = input("\nTry again? [y/n]: \n")
                        if (option == "y"):
                            break
                        elif (option == "n"):
                            return 2
                        else:
                            print("\nINVALID OPTION!\n")


    elif (option == "9"):
        return -1
    elif (option == "0"):
        return 1
    else:
        print("\nINVALID OPTION!\n")


# Main Function
def main():
    isDataFilled:bool = False # Indicates if there is data already being inputed

    linReg:LinReg = LinReg() # Instantiate LinReg Object
    expReg:ExpReg = ExpReg() # Instantiate ExpReg Object
    polReg:PolReg = PolReg() # Instantiate PolReg Object

    while (True):
        option:int = 0 # The option

        # Main Menu
        print("\n\n\n=== Main Menu ===")
        print("[1] Add Data\n[2] Plot\n[3] Find Best Fit\n[0] Exit")
        option = input("Please input option: ")


        # First option (Add Data Menu)
        if (option == "1"):
            while (True):
                print("\n\n=== Add Data ===")
                print("[1] Add Manually\n[2] Add from CSV file\n[3] Add from formated CSV file\n[9] Back\n[0] Exit")
                option = input("Please input option: ")
                
                result = menuAddData(option, linReg, expReg, polReg)
                if (result == 0):
                    isDataFilled = True
                elif (result == -1):
                    break
                elif (result == 1):
                    return 0
                else:
                    pass
                

        # Second Option (Plot Data Menu)
        elif (option == "2"):
            if (not isDataFilled):
                print("\nDATA IS EMPTY!\n")
                continue
            while (True):
                print("\n\n=== Plot Data ===")
                print("[1] Linear Regression\n[2] Exponential Regression\n[3] Polynomial Regression\n[4] Plot All\n[9] Back\n[0] Exit")
                option = input("Please input option: ")

                if (option == "1"):
                    linReg.plot()
                elif (option == "2"):
                    expReg.plot()
                elif (option == "3"):
                    polReg.plot()
                elif (option == "4"):
                    plot(linReg.getXList(), linReg.getYList(), linReg.getReg(), expReg.getReg(), polReg.getReg())
                elif (option == "9"):
                    break
                elif (option == "0"):
                    return 0
                else:
                    print("\nINVALID OPTION!\n")

        
        # Third Option (Find Fittest Regression Method)
        elif (option == "3"):
            if (not isDataFilled):
                print("\nDATA IS EMPTY!\n")
                continue
            
            linStdErr:float = float(linReg.getStdError())
            expStdErr:float = float(expReg.getStdError())
            polRegErr:dict = polReg.getStdError()

            fittestMethod:str = ""
            tempValue:float = 0.0
            if (linStdErr < expStdErr):
                fittestMethod = "Linear Regression"
                tempValue = linStdErr
            else:
                fittestMethod = "Exponential Regression"
                tempValue = expStdErr

            for key in polRegErr:
                if (float(polRegErr[key]) < tempValue):
                    fittestMethod = f"Polynomial Regression order {key}"
                    tempValue = float(polRegErr[key])
            
            print(f"\nThe fittest regression method is {fittestMethod} with a standard error of {tempValue}\n")
            
        elif (option == "0"):
            return 0
        else:
            print("\nINVALID OPTION!\n")


# Execute the main function
main()