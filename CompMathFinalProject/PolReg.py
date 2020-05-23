import numpy as np
from decimal import Decimal as Dec
from decimal import DecimalException

from Reg import Reg


class PolReg(Reg):
    __order:int

    __coeffList:np.ndarray
    __regList:np.ndarray
    __stdErr:Dec = Dec("0")




    def __calcPolReg(self):
        self.__coeffList = self._calcCoeff(self._xList, self._yList, self.__order)
        self.__regList = self._calcReg(self._xList, self.__coeffList, self.__order)
        self.__stdErr = self._calcStdErr(self._yList, self.__regList)


    # Inserting xList and yList
    def insertList(self, xList:np.ndarray, yList:np.ndarray = np.array([]), order:int = 2):
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
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    # Set the number of data points
                    self._numOfData = self._xList.size
                    self.__order = order
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
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    # Set the number of data points
                    self._numOfData = self._xList.size
                    self.__order = order
                    self.__calcPolReg()
                    return 0
        return -1

    
    # Get linear coefficient
    def getCoeff(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regList


    # Get standard error
    def getStdError(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__stdErr


    # Get list of y axes in linear regression line
    def getReg(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__regList


    # Predict y axes at linear regression with given x
    def f(self, x:float):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        x:Dec = Dec(str(x))
        power:np.ndarray = np.arange(0, 1 + 1, dtype = Dec)

        return np.multiply(np.power(np.full(1 + 1, x), power), self.__coeffList.transpose()).sum()