import numpy as np
from decimal import Decimal as Dec

class Reg:
    # Data
    _numOfData:int = 0

    _xList:np.ndarray = np.array([])
    _yList:np.ndarray = np.array([])




    # Calculates standard error
    def _calcStdErr(self, yList:np.ndarray, regList:np.ndarray):
        return np.sqrt(np.power(np.subtract(regList, yList), 2).sum() / (yList.size - 2))


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
        coeffList:np.ndarray = np.ones((matrixSize, 1), dtype = Dec) # List of coefficient
        for i in range(matrixSize):
            value:Dec = Dec("0") # The value of total sum of rows in x matrix
            for j in range(i+1):
                if (i == j):
                    coeffList[matrixSize - j - 1][0] = (yMatrix[matrixSize - i - 1][0] - value) / xMatrix[matrixSize - i - 1][matrixSize - j - 1]
                    break
                value += xMatrix[matrixSize - i - 1][matrixSize - j - 1] * coeffList[matrixSize - j - 1][0]
        return coeffList


    # Calculates coefficient
    def _calcCoeff(self, xList:np.ndarray, yList:np.ndarray, order:int):
        size:int = order + 1 # Size of matrix based on the order
        temp:list = [Dec(self._numOfData)] # List of powered x with initial n (size of xList)
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
        
        # Calculating the coefficient
        return self.__linAlg(xMatrix, yMatrix, order)


    # Calculates y axes in polynomial regression line of given x axes
    def _calcReg(self, xList:np.ndarray, coeffList:np.ndarray, order:int):
        tempMatrix:np.ndarray = np.multiply(np.ones((order + 1, self._numOfData), dtype = Dec), xList).transpose() # Create temporary matrix for list of x
        power:np.ndarray = np.arange(0, order + 1, dtype = Dec) # The power of the x
        tempMatrix[:,0][tempMatrix[:,0] == 0] = Dec(1)

        return np.sum(np.multiply(np.power(tempMatrix, power), coeffList.transpose()), axis = 1)




    # Get the number of data (number of data points)
    def getSize(self):
        return self._numOfData


    # Get list of x axes
    def getXList(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self._xList


    # Get list of y axes
    def getYList(self):
        if (self._numOfData == 0):
            print("Empty List! Please insert list beforehand!")
            return np.array([])
        return self._yList
    