import numpy as np
from coinlib.helper import log
import pandas as pd

class BasicJob:
    def __init__(self, df, inputs):
        self.df = df
        self.inputs = inputs
        self.uniqueName = ""
        self.features = self
        pass

        ## gets a signal data

    def set(self, name, data, index=None, symbol=None):

        name = self.getUniqueName()+":"+name
        if data is not None:
            self.df.loc[self.df.index[-1], "session:" + name] = data

        return self.df.loc[self.df.index[-1]]["session:" + name]

    def getOutputCol(self):
        return "result"

    def result(self, resultList, colname=None, fillType="front"):

        if isinstance(resultList, np.ndarray):
            resultList = np.pad(resultList, (self.df.shape[0] - len(resultList), 0), 'constant', constant_values=(np.nan))

        self.df[self.getOutputCol()] = resultList

        return self.df[self.getOutputCol()]

    ## This method adds a signal
    def signal(self, name, data=None, index=-1, symbol=None):

        name = self.getUniqueName()+":"+name
        if "session:" + name not in self.df.columns:
            self.df["session:" + name] = None

        if data is not None:
            self.df.loc[self.df.index[index], "session:" + name] = data

        if "session:" + name in self.df.columns:
            data = self.df.loc[self.df.index[index]]["session:" + name]

        return data

    def getInputValue(self, input):

        if isinstance(input, dict):
            if "value" in input:
                return input["value"]

        return input

    def get(self, name, index=None):

        data = None
        try:
                # if its a key of inputs - lets export the right column
                if name in self.inputs:
                    if isinstance(self.inputs[name], str):
                        return self.get(self.getInputValue(self.inputs[name]), index)
                    if self.inputs[name]["type"] == "dataInput":
                        return self.get(self.getInputValue(self.inputs[name]["value"]), index)

                data = None
                if name + ":y" in self.df.columns:
                    data = self.df[name + ":y"]
                elif "additionalData."+name in self.df.columns:
                    data = self.df["additionalData."+name]
                elif name + ":close" in self.df.columns:
                    data = self.df[name + ":close"]
                elif "session:" + name in self.df.columns:
                    data = self.df["session:" + self.getUniqueName()+":"+name]
                elif name in self.df.columns:
                    data = self.df[name]
                else:
                    data = self.inputs[name]
        except Exception as e:
            log.error(e)


        return data

    def getAsArray(self, name, index=None):

        data = self.get(name, index=index)

        return data.values

    ## This method combines all params and combine as a dataframe
    def df(self):
        return self.df

    def setVar(self, name, data):

        return self.var(name, data)

    def setUniqueName(self, name):
        self.uniqueName = name
        return name

    def getUniqueName(self):
        return self.uniqueName

    def price(self, chart="chart1"):
        currentSlot = self.df.loc[self.df.index[-1]]

        return currentSlot[chart+".main:close"]

    def isNaN(self, num):
        return num != num

    def additional(self, name):

        index = -1

        if "additionalData." + name in self.df.columns:
            data = self.df.loc[self.df.index[index], "additionalData." + name]
            if self.isNaN(data):
                return None
            return data

        return None

    def date(self):
        return self.time()

    def time(self):
        date = pd.to_datetime(self.df.index[-1])
        return date

    ## This method adds a signal
    def var(self, name, data=None):

        index = -1

        name = self.getUniqueName()+":"+name
        if "session:" + name not in self.df.columns:
            self.df["session:" + name] = None

        if data is not None:
            self.df.loc[self.df.index[index], "session:" + name] = data
        else:
            index = -2

        if "session:" + name in self.df.columns:
            data = self.df.loc[self.df.index[index]]["session:" + name]

        return data

