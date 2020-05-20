import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from decimal import Decimal as Dec
import decimal

class LinReg:
    __n:int = 0 # Number of data points

    __polOrder:int = 2
    __polConstant:np.ndarray = np.array([])

    # Data
    __xList:np.ndarray = np.array([])
    __yList:np.ndarray = np.array([])

    # Calculates polynomial constant
    def __calcPolConstant(self):
        size:int = self.__polOrder + 1
        temp:list = [self.__n] # List of powered x with initial n (size of xList)
        xMatrix:np.ndarray = np.zeros((size, size)) # Create a zero 2D matrix
        yMatrix:np.ndarray = np.zeros((size, 1)) # Create a zero 1D matrix
            
        # Filling temp with powered x
        for i in range(1, 2 * size):
            temp.append(np.sum(np.power(self.__xList,i)))

        # Filling zero 2D matrix (xMatrix) with the powered x in temp
        for i in range(size):
            xMatrix[i] = temp[i : i + size]
            
        # Filling zero 1D matrix (yMatrix)
        for i in range(size):
            if (i == 0):
                yMatrix[i][0] = np.sum(self.__yList)
            else:
                yMatrix[i][0] = np.sum(np.multiply(self.__yList, np.power(self.__xList, i)))
        
        # Calculating the constants (a)
        self.__polConstant = np.dot(np.linalg.inv(xMatrix),yMatrix) 

    # Inserting xList and yList
    def insertList(self, xList:np.ndarray, yList:np.ndarray = np.array([])):
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
                # Return -1 if xList does not contains numpy.ndarray, which means there is at least one data has different size (turns np.ndarray type to list)
                # Return -1 if coordinate has insufficient or extra axes
                print("Invalid Amount of Axes! A Coordinate must only contain (x,y) axes!")
            else:
                # Make input x and y axes in coordinateList as object's variable (converts int, string, or float to Decimal data type)
                try:
                    self.__xList = np.array([Dec(str(coord[0])) for coord in xList], dtype = Dec)
                    self.__yList = np.array([Dec(str(coord[1])) for coord in xList], dtype = Dec)
                    return 0
                except decimal.DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    self.__n = self.__xList.size
                    self.__calcLinGradient()
                    self.__calcLinConstant()
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
                # Make input xList and yList as object's variable (converts int, string, or float to Decimal data type)
                try:
                    self.__xList = np.array([Dec(str(x)) for x in xList], dtype = Dec)
                    self.__yList = np.array([Dec(str(y)) for y in yList], dtype = Dec)
                    return 0
                except decimal.DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    self.__n = self.__xList.size
                    self.__calcLinGradient()
                    self.__calcLinConstant()
        return -1

    # Get list of x axes
    def getXList(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__xList

    # Get list of y axes
    def getYList(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__yList


    # Get size of data (number of data points)
    def getSize(self):
        return self.__n

    def getPolOrder(self):
        return self.__polOrder

    def getPolConstant(self):
        self.__calcPolConstant
        print(self.__polConstant)

    # def getLinReg():
    #     m


    # def plotGraph():
    #     return
