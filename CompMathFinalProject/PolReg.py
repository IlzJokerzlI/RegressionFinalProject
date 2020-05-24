import sys
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal as Dec
from decimal import DecimalException
from matplotlib.ticker import FixedLocator, AutoMinorLocator

from Reg import Reg


class PolReg(Reg):
    # Data
    __minOrder:int
    __maxOrder:int

    __coeffDict:dict = {}
    __regDict:dict = {}
    __stdErrDict:dict = {}




    # Polynomial regression calculations
    def __calcPolReg(self):
        for order in range(self.__minOrder, self.__maxOrder + 1):
            self.__coeffDict[str(order)] = self._calcCoeff(self._xList, self._yList, order)
            self.__regDict[str(order)] = self._calcReg(self._xList, self.__coeffDict[str(order)], order)
            self.__stdErrDict = self._calcStdErr(self._yList, self.__regDict[str(order)])


    # Inserting xList and yList
    def insertList(self, xList:np.ndarray, yList:np.ndarray = np.array([]), minOrder:int = 2, maxOrder = 2):
        if (not isinstance(xList, np.ndarray) or not isinstance(yList, np.ndarray)):
            # Return -1 if xList or yList is not numpy.ndarray type
            print("Invalid lists type! Must be numpy.ndarray type!")
            return -1

        if (len(yList) == 0):
            # Conditions for coordinateList input
            if (len(xList) == 0):
                # Return -1 if both xList and yList are empty
                print("Empty List!")
            elif (len(xList) < 3):
                # Return -1 if the data in the lists are less than 3 (results in insufficient data)
                print("Insufficient data in lists!")
                return 0
            elif (not isinstance(xList[0], np.ndarray) or len(xList[0]) != 2):
                # Return -1 if xList's elements are not numpy.ndarray, which means there is at least one data has different size (turns np.ndarray type to list)
                # Return -1 if coordinate has insufficient or extra axes
                print("Invalid Amount of Axes! A Coordinate must only contain (x,y) axes!")
            else:
                try:
                    # Make input x and y axes in coordinateList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(coord[0])) for coord in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(coord[1])) for coord in xList], dtype = Dec)

                    if (minOrder < 2):
                        self.__minOrder = 2
                    else:
                        self.__minOrder = minOrder


                    if (maxOrder < self.__minOrder):
                        self.__maxOrder = self.__minOrder
                    else:
                        self.__maxOrder = maxOrder


                    # Set the number of data points
                    self._numOfData = len(self._xList)
                    self.__calcPolReg()
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                except:
                    print("Unexpected error!")
                    print(sys.exc_info()[0])
                    return np.array([]), np.array([])
        else:
            # Conditions for xList and yList input
            if (True in [isinstance(x, (list, tuple, dict, np.ndarray)) for x in xList] or True in [isinstance(y, (list, tuple, dict, np.ndarray)) for y in yList]):
                # Return -1 if type list, tuple, dict, or numpy.ndarray exist in either xList of yList
                print("Lists contain invalid data type!")
            elif (len(xList) != len(yList)):
                # Return -1 if xList is not the same size as yList
                print("Lists are unaligned!")
            elif (len(xList) < 3):
                # Return -1 if the data in the lists are less than 3 (results in insufficient data)
                print("Insufficient data in lists!")
            else:
                try:
                    # Make input xList and yList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(x)) for x in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(y)) for y in yList], dtype = Dec)

                    if (minOrder < 2):
                        # Check if minimum order is less than 2
                        self.__minOrder = 2
                    else:
                        self.__minOrder = minOrder


                    if (maxOrder < self.__minOrder):
                        # Check if maximum order is less than minimum order
                        self.__maxOrder = self.__minOrder
                    else:
                        self.__maxOrder = maxOrder


                    # Set the number of data points
                    self._numOfData = len(self._xList)
                    self.__calcPolReg()
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                except:
                    print("Unexpected error!")
                    print(sys.exc_info()[0])
                    return np.array([]), np.array([])
        return -1

    
    # Get coefficient
    def getCoeff(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__coeffDict


    # Get standard error
    def getStdError(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__stdErrDict


    # Get list of y axes of regression line
    def getReg(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regDict


    # Predict y axes at regression line with given x
    def f(self, x:float, order:int):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])

        if (not (str(order) in self.__coeffDict)):
            # Check if the order is exist in the list
            print(f"Coefficient with order of {order} does not exist! Please re-insert the data by including order {order}!")


        x:Dec = Dec(str(x)) # Change the type to Decimal
        power:np.ndarray = np.arange(0, 1 + 1, dtype = Dec) # The power of x
        tempList:np.ndarray = np.full(1 + 1, x, dtype = Dec)
        if (tempList[0] == 0):
            # Change first index value to 1 if it is 0, Dec(0)**Dec(0) produces error
            tempList[0] = Dec("1")

        return np.multiply(np.power(tempList, power), self.__coeffDict[str(order)].transpose()).sum()


    # Plot
    def plot(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return -1
        xList = self._xList.astype(float)
        yList = self._yList.astype(float)

        fig, ax = plt.subplots(figsize = (20,15))

        # Title
        ax.set_title(f"Linear Regression Graph\nrange({xList.min()} - {xList.max()})")

        # Plot line graph
        for key in self.__regDict:
            ax.plot(xList, self.__regDict[key].astype(float),
                    label = f"Order {key}",
                    marker = "x",
                    markersize = 10,
                    zorder = 0.5)
                
        # Plot scatter graph
        ax.scatter(xList, yList,
                   label = "Sample Data",
                   marker = "o",
                   s = 30,
                   c = "red",
                   alpha = 0.8,
                   zorder =1)

        # Legend
        ax.legend(title = "Legend",
                  fontsize = "large")

        # Grid
        ax.grid(which = "both")

        # Ticks
        ax.xaxis.set_major_locator(FixedLocator(xList))
        ax.yaxis.set_major_locator(FixedLocator(yList))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(10))

        plt.show()
        return 0