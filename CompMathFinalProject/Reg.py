import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from decimal import Decimal as Dec
from decimal import DecimalException

class Reg:
    # Data
    __n:int = 0 # Number of data points
    __xList:np.ndarray = np.array([])
    __yList:np.ndarray = np.array([])

    # Linear
    __linConstant:np.ndarray = np.array([])
    __yLinRegList:np.ndarray = np.array([])

    # Polynomial
    __polOrder:int
    __polConstant:np.ndarray = np.array([])
    __yPolRegList:np.ndarray = np.array([])

    # Exponential
    __expConstant:np.ndarray = np.array([])
    __yExpRegList:np.ndarray = np.array([])
    


    # Constructor
    def __init__(self, polOrder = 2):
        if (polOrder >= 2):
            self.__polOrder = polOrder
        else:
            self.__polOrder = 2




    # Naive Gauss Elimination Linear Algebra
    def __linAlg(self, xMatrix:np.ndarray, yMatrix:np.ndarray, order:int):
        matrixSize:int = order + 1 # The size of matrix

        # Forward Elimination
        tempMatrix = np.concatenate((xMatrix, yMatrix), axis = 1) # Temporary matrix by concatenating x and y matrix
        for i in range(matrixSize):
            for j in range(i + 1, matrixSize):
                temp = tempMatrix[j][i] / tempMatrix[i][i]
                tempMatrix[j] = tempMatrix[j] - (np.multiply(tempMatrix[i], temp))
        
        # Seperate tempMatrix back into x and y matrix accordingly
        xMatrix:np.ndarray = tempMatrix[:, :-1]
        yMatrix:np.ndarray = tempMatrix[:, -1].reshape((matrixSize, 1))
        
        # Backward Substitution
        constantList:np.ndarray = np.ones((matrixSize, 1), dtype = Dec) # List of constants
        for i in range(matrixSize):
            value:Dec = Dec("0") # The value of total sum of rows in x matrix
            for j in range(i+1):
                if (i == j):
                    constantList[matrixSize - j - 1][0] = (yMatrix[matrixSize - i - 1][0] - value) / xMatrix[matrixSize - i - 1][matrixSize - j - 1]
                    break
                value += xMatrix[matrixSize - i - 1][matrixSize - j - 1] * constantList[matrixSize - j - 1][0]
        return constantList


    # Calculates constant
    def __calcConstant(self, xList:np.ndarray, yList:np.ndarray, order:int):
        size:int = order + 1 # Size of matrix based on the order
        temp:list = [Dec(self.__n)] # List of powered x with initial n (size of xList)
        xMatrix:np.ndarray = np.zeros((size, size), dtype = Dec) # Create a zero 2D matrix
        yMatrix:np.ndarray = np.zeros((size, 1), dtype = Dec) # Create a zero 1D matrix
            
        # Filling temp with powered x
        for i in range(1, 2 * size):
            temp.append(np.sum(np.power(xList,i)))

        # Filling zero 2D matrix (xMatrix) with the powered x in temp
        for i in range(size):
            xMatrix[i] = temp[i : i + size]
            
        # Filling zero 1D matrix (yMatrix)
        for i in range(size):
            if (i == 0):
                yMatrix[i][0] = np.sum(yList)
            else:
                yMatrix[i][0] = np.sum(np.multiply(yList, np.power(xList, i)))
        
        # Calculating the constants
        return self.__linAlg(xMatrix, yMatrix, order)


    # Calculates y axes in polynomial regression line of given x axes
    def __calcReg(self, xList:np.ndarray, constant:np.ndarray, order:int):
        tempMatrix:np.ndarray = np.multiply(np.ones((order + 1, self.__n), dtype = Dec), xList).transpose() # Create temporary matrix for list of x
        power:np.ndarray = np.arange(0, order + 1, dtype = Dec) # The power of the x

        return np.sum(np.multiply(np.power(tempMatrix, power), constant.transpose()), axis = 1)


    def __calcLinReg(self):
        self.__linConstant = self.__calcConstant(self.__xList, self.__yList, 1)
        self.__yLinRegList = self.__calcReg(self.__xList, self.__linConstant, 1)


    def __calcPolReg(self):
        self.__polConstant = self.__calcConstant(self.__xList, self.__yList, self.__polOrder)
        self.__yPolRegList = self.__calcReg(self.__xList, self.__polConstant, self.__polOrder)


    # def __calcExpReg(self):
    #     self.__expConstant = self.__calcConstant(self.__xList, self.__yList, 1)


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
                # Return -1 if xList's elements are not numpy.ndarray, which means there is at least one data has different size (turns np.ndarray type to list)
                # Return -1 if coordinate has insufficient or extra axes
                print("Invalid Amount of Axes! A Coordinate must only contain (x,y) axes!")
            else:
                try:
                    # Make input x and y axes in coordinateList as object's variable (converts int, string, or float to Decimal data type)
                    self.__xList = np.array([Dec(str(coord[0])) for coord in xList], dtype = Dec)
                    self.__yList = np.array([Dec(str(coord[1])) for coord in xList], dtype = Dec)
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    # Set the number of data points
                    self.__n = self.__xList.size
                    self.__calcLinReg()
                    self.__calcPolReg()
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
                    self.__xList = np.array([Dec(str(x)) for x in xList], dtype = Dec)
                    self.__yList = np.array([Dec(str(y)) for y in yList], dtype = Dec)
                    return 0
                except DecimalException as e:
                    # Catch unknown error from Decimal object
                    print(f"Error: {str(e)}")
                finally:
                    # Set the number of data points
                    self.__n = self.__xList.size
                    self.__calcLinReg()
                    self.__calcPolReg()
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


    # Get polinomial order
    def getPolOrder(self):
        return self.__polOrder


    # Set Polinomial order
    def setPolOrder(self, order:int):
        if (order < 2):
            print("Order must not be less than 2!")
            return -1
        self.__polOrder = order
        return 0


    # Get linear constant
    def getLinConstant(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__linConstant


    # Get polinomial constant
    def getPolConstant(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__polConstant


    # Get list of y axes in linear regression line
    def getYLinReg(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__yLinRegList


    # Get list of y axes in polynomial regression line
    def getYPolReg(self):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self.__yPolRegList


    # Predict y axes at linear regression with given x
    def getLinF(self, x:float):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        x:Dec = Dec(str(x))
        power:np.ndarray = np.arange(0, 1 + 1, dtype = Dec)

        return np.multiply(np.power(np.full(1 + 1, x), power), self.__polConstant.transpose()).sum()


    # Predict y axes at polynomial regression with given x
    def getPolF(self, x:float):
        if (self.__n == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        x:Dec = Dec(str(x))
        power:np.ndarray = np.arange(0, self.__polOrder + 1, dtype = Dec)

        return np.multiply(np.power(np.full(self.__polOrder + 1, x), power), self.__polConstant.transpose()).sum()

    # def plotGraph():
    #     return
