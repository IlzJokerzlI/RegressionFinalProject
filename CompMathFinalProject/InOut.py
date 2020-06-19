import csv
import sys
import numpy as np
import pandas as pd

"""
    InOut Class

    Used to contain all input and output activities. It currently supports csv file with 2 types of format. The first one being the standard format and the other one being complex format. The standard format only applies to its own type and so dies the complex format which only applies to the {covid_19_data.csv} format. The line { series:pd.Series = data.set_index("COLUMN NAME").transpose()["ROW NAME"][3:] } has 2 changeable parameters however it remains fixed in this program. COLUMN NAME is the name of the column (Country/Region) and ROW NAME is the specific row title (Taiwan*), so it will retrieve the data from that specific row.
"""
class InOut:
    # Reads a file from a file name
    def readStandard(self, fileName:str):
        # Try-Catch
        try:
            data:np.ndarray = np.genfromtxt(fileName, delimiter = ",") # Retrieves data by seperating it by comma(,)
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
        # Try-Catch
        try:
            data:pd.DataFrame = pd.read_csv(fileName) # Reads csv
            series:pd.Series = data.set_index("Country/Region").transpose()["Taiwan*"][3:] # Gets the specific row of dataframe and extracts it
            series.index = np.arange(1,np.size(series)+1) # Set index of series
            xList:np.ndarray = np.array(series.index, dtype = float) # Gets the index and converts it to float
            yList:np.ndarray = np.array(list(series), dtype = float) # Gets the values and converts it to float
            return xList, yList
            
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