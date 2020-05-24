import csv
import sys
import numpy as np

class InOut:
    def read(self, fileName:str):
        try:
            data = np.genfromtxt(fileName, delimiter = ",")
            data = data[~np.isnan(data).any(axis= 1)]
            return data[:,0], data[:,1]
        except IOError as err:
            print("File not found!")
            print(err.args[0])
            return np.array([]), np.array([])
        except ValueError as err:
            print("Value error")
            print(err.args[0])
            return np.array([]), np.array([])
        except:
            print("Unexpected error!")
            print(sys.exc_info()[0])
            return np.array([]), np.array([])
