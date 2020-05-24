import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal as Dec
from decimal import DecimalException
from matplotlib.ticker import FixedLocator, AutoMinorLocator

from Reg import Reg


class PolReg(Reg):
    __minOrder:int
    __maxOrder:int

    __coeffDict:dict = {}
    __regDict:dict = {}
    __stdErrDict:dict = {}




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

        if (yList.size == 0):
            # Conditions for coordinateList input
            if (xList.size == 0):
                # Return -1 if both xList and yList are empty
                print("Empty List!")
            elif (not isinstance(xList[0], np.ndarray) or xList[0].size != 2):
                # Return -1 if xList's elements are not numpy.ndarray, which means there is at least one data has different size (turns np.ndarray type to list)
                # Return -1 if coordinate has insufficient or extra axes
                print("Invalid Amount of Axes! A Coordinate must only contain (x,y) axes!")
            else:
                try:
                    # Make input x and y axes in coordinateList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(coord[0])) for coord in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(coord[1])) for coord in xList], dtype = Dec)
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    # Set the number of data points
                    self._numOfData = self._xList.size
                    self.__calcPolReg()
                    return 0
        else:
            # Conditions for xList and yList input
            if (True in [isinstance(x, (list, tuple, dict, np.ndarray)) for x in xList] or True in [isinstance(y, (list, tuple, dict, np.ndarray)) for y in yList]):
                # Return -1 if type list, tuple, dict, or numpy.ndarray exist in either xList of yList
                print("Lists contain invalid data type!")
            elif (xList.size != yList.size):
                # Return -1 if xList is not the same size as yList
                print("Lists are unaligned!")
            elif (xList.size < 2):
                # Return -1 if the data in the lists are less than 2 (results in insufficient data)
                print("Insufficient data in lists!")
            else:
                try:
                    # Make input xList and yList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(x)) for x in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(y)) for y in yList], dtype = Dec)
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    if (minOrder < 2):
                        self.__minOrder = 2
                    else:
                        self.__minOrder = minOrder


                    if (maxOrder < self.__minOrder):
                        self.__maxOrder = self.__minOrder
                    else:
                        self.__maxOrder = maxOrder


                    # Set the number of data points
                    self._numOfData = self._xList.size
                    self.__calcPolReg()
                    return 0
        return -1

    
    # Get linear coefficient
    def getCoeff(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regDict


    # Get standard error
    def getStdError(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__stdErrDict


    # Get list of y axes in linear regression line
    def getReg(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regDict


    # Predict y axes at linear regression with given x
    def f(self, x:float, order:int):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])

        if (not (str(order) in self.__coeffDict)):
            print(f"Coefficient with order of {order} does not exist! Please re-insert the data by including order {order}!")


        x:Dec = Dec(str(x))
        power:np.ndarray = np.arange(0, 1 + 1, dtype = Dec)

        return np.multiply(np.power(np.full(1 + 1, x), power), self.__coeffDict[str(order)].transpose()).sum()


    # Plot
    def plot(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return -1
        xList = self._xList.astype(float)
        yList = self._yList.astype(float)

        fig, ax = plt.subplots(figsize = (20,15))

        for key in self.__regDict:
            ax.plot(xList, self.__regDict[key].astype(float),
                    label = f"Order {key}",
                    marker = "x",
                    markersize = 10,
                    zorder = 0.5)
                
        ax.scatter(xList, yList,
                   label = "Sample Data",
                   marker = "o",
                   s = 30,
                   c = "red",
                   alpha = 0.8,
                   zorder =1)

        ax.legend(title = "Legend",
                  fontsize = "large")

        ax.grid(which = "both")
        ax.xaxis.set_major_locator(FixedLocator(xList))
        ax.yaxis.set_major_locator(FixedLocator(yList))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(10))

        plt.show()
        return 0