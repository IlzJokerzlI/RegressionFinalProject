import csv
import sys
import numpy as np

"""
    InOut Class

    Used to contain all input and output activities. It currently only supports reading and only one type of .txt type file
"""
class InOut:
    # Reads a file from a file name
    def read(self, fileName:str):
        # Try-Catch
        try:
            data = np.genfromtxt(fileName, delimiter = ",") # Retrieves data by seperating it by comma(,)
            data = data[~np.isnan(data).any(axis= 1)] # Skips if it is empty
            return data[:,0], data[:,1]
        except IOError as err:
            # Catches error when a file is not found
            print("File not found!")
            print(err.args[0])
            return np.array([]), np.array([])
        except ValueError as err:
            # Catches error if there is any unwanted character in the data
            print("Value error")
            print(err.args[0])
            return np.array([]), np.array([])
        except:
            # Catches other errors
            print("Unexpected error!")
            print(sys.exc_info()[0])
            return np.array([]), np.array([])
