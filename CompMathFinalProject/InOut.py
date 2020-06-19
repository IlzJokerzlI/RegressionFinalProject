import csv
import sys
import numpy as np
import pandas as pd

"""
    InOut Class

    Used to contain all input and output activities. It currently only supports reading and only one type of .txt type file
"""
class InOut:
    # Reads a file from a file name
    def readStandard(self, fileName:str):
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


    # Reads a more complex file from a file name
    def readComplex(self, fileName:str):
        data:pd.DataFrame = pd.read_csv("time_series_covid19_confirmed_global.csv") # Read csv
        series:pd.Series = data.set_index("Country/Region").transpose()["Taiwan*"][3:] # Getting the specific row of dataframe
        series.index:pd.Series = np.arange(1,np.size(series)+1) # Set index of series
        xList:np.ndarray = np.array(series.index, dtype=str) # Change index to type string
        yList:np.ndarray = np.array(series.astype(str).apply(lambda y: "," + y), dtype=str) # Converts to string and manipulates series values by adding comma (,) before it.
        result = np.core.defchararray.add(xList, yList) # Combines x values and y values
        np.savetxt("Test.csv", result, delimiter ="",fmt='%s') # Output to .csv file
