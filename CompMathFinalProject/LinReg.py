import sys
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal as Dec
from decimal import DecimalException
from matplotlib.ticker import FixedLocator, AutoMinorLocator

from Reg import Reg


"""
    LinReg Class

    LinReg stands for Linear Regression, it is a class that inherits from Reg class and specialized for handling linear regression. Linear regression has a formula of {y = mx + c} where m is the gradient and c is the constant. Being the first order polynomial regression, the linear regression has less rules when compared to polynomial regression as well as exponential regression.
"""
class LinReg(Reg):
    # Data
    __order:int = 1 # The linear regression is the first order of polynomial

    __coeffList:np.ndarray # Stores the list of coefficients namely the gradient(m) and constant(c)
    __regList:np.ndarray # Stores the list of regression values
    __stdErr:Dec = Dec("0") # Stores the standard error




    # Linear regression calculations
    def __calcLinReg(self):
        self.__coeffList = self._calcCoeff(self._xList, self._yList, self.__order) # Calculates the coefficients of linear regression namely gradient(m) and constant(c)
        self.__regList = self._calcReg(self._xList, self.__coeffList, self.__order) # Calculates the regression values
        self.__stdErr = self._calcStdErr(self._yList, self.__regList) # Calculates and assigns the standard error


    # Inserting xList and yList
    def insertList(self, xList:np.ndarray, yList:np.ndarray = np.array([])):
        if (not isinstance(xList, np.ndarray) or not isinstance(yList, np.ndarray)):
            # Return -1 if xList or yList is not numpy.ndarray type
            print("Invalid lists type! Must be numpy.ndarray type!")
            return -1

        if (len(yList) == 0):
            # Conditions for coordinateList input
            if (len(xList) == 0):
                # Return -1 if both xList and yList are empty
                print("Empty List!")
            elif (len(xList) < 2):
                # Return -1 if the data in the lists are less than 2 (results in insufficient data)
                print("Insufficient data in lists!")
            elif (not isinstance(xList[0], np.ndarray) or len(xList[0]) != 2):
                # Return -1 if xList's elements are not numpy.ndarray, which means there is at least one data has different size (turns np.ndarray type to list)
                # Return -1 if coordinate has insufficient or extra axes
                print("Invalid Amount of Axes! A Coordinate must only contain (x,y) axes!")
            else:
                try:
                    # Make input x and y axes in coordinateList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(coord[0])) for coord in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(coord[1])) for coord in xList], dtype = Dec)

                    # Set the number of data points
                    self._numOfData = len(self._xList)
                    self.__calcLinReg()
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
            elif (len(xList) < 2):
                # Return -1 if the data in the lists are less than 2 (results in insufficient data)
                print("Insufficient data in lists!")
            else:
                try:
                    # Make input xList and yList as object's variable (converts int, string, or float to Decimal data type)
                    self._xList = np.array([Dec(str(x)) for x in xList], dtype = Dec)
                    self._yList = np.array([Dec(str(y)) for y in yList], dtype = Dec)

                    # Set the number of data points
                    self._numOfData = len(self._xList)
                    self.__calcLinReg()
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
        return self.__coeffList


    # Get standard error
    def getStdError(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__stdErr


    # Get list of y axes of regression line
    def getReg(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regList


    # Predict y axes at regression line with given x
    def f(self, x:float):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        x:Dec = Dec(str(x)) # Change the type to Decimal
        power:np.ndarray = np.arange(0, 1 + 1, dtype = Dec) # The power of x
        tempList:np.ndarray = np.full(1 + 1, x, dtype = Dec)
        if (tempList[0] == 0):
            # Change first index value to 1 if it is 0, Dec(0)**Dec(0) produces error
            tempList[0] = Dec("1")

        return np.multiply(np.power(tempList, power), self.__coeffList.transpose()).sum()

    
    # Plot
    def plot(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return -1
        xList = self._xList.astype(float) # Change type to float
        yList = self._yList.astype(float) # Change type to float
        regList = self.__regList.astype(float) # Change type to float

        fig, ax = plt.subplots(figsize = (20,15))

        # Set title
        ax.set_title(f"Linear Regression Graph\nrange({xList.min()} - {xList.max()})")

        # Plot line graph
        ax.plot(xList, regList,
                label = "Linear Regression Line",
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