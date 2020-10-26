import pandas as pd
import numpy as np


class CostOptimizer:
    def __init__(self, material):
        self.material = material

        self.__load_data()
        self.__build_graph()

    def run(self):
        return self.edgeArr

    @staticmethod
    def __get_min_indicator(dict, idx):
        arr = []

        for key, values in dict.items():
            if key == "material ID":
                arr.append(values[idx])
            elif key == "level":
                arr.append(values[idx])
            elif key == "description":
                arr.append(values[idx])
            elif key == "category":
                arr.append(values[idx])
            elif key == "hierarchy category":
                arr.append(values[idx])
            elif key == "price":
                arr.append(values[idx])

        return arr

    def __prepare_graph_data(self):
        self.edgeArr = []
        self.edgeArr.append(self.__get_min_indicator(self.engine, self.engineDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.alternator, self.alternatorDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.piston, self.pistonDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.oil_pump, self.oil_pumpDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.engine_frame, self.engine_frameDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.alternator_fan, self.alternator_fanDF["price"].idxmin()))
        self.edgeArr.append(self.__get_min_indicator(self.electrical_ring, self.electrical_ringDF["price"].idxmin()))
        self.edgeArr.append(
            self.__get_min_indicator(self.alternator_skeleton, self.alternator_skeletonDF["price"].idxmin()))

    def __build_graph(self):
        self.__prepare_graph_data()

    def __load_data(self):
        self.engineDF = pd.read_csv("../data/raw/engine.csv")
        self.alternatorDF = pd.read_csv("../data/raw/alternator.csv")
        self.pistonDF = pd.read_csv("../data/raw/pistons.csv")
        self.oil_pumpDF = pd.read_csv("../data/raw/oil_pump.csv")
        self.engine_frameDF = pd.read_csv("../data/raw/frame.csv")
        self.alternator_fanDF = pd.read_csv("../data/raw/alternator_fan.csv")
        self.electrical_ringDF = pd.read_csv("../data/raw/electrical_ring.csv")
        self.alternator_skeletonDF = pd.read_csv("../data/raw/alternator_skeleton.csv")

        self.engine = pd.read_csv("../data/raw/engine.csv").to_dict()
        self.alternator = pd.read_csv("../data/raw/alternator.csv").to_dict()
        self.piston = pd.read_csv("../data/raw/pistons.csv").to_dict()
        self.oil_pump = pd.read_csv("../data/raw/oil_pump.csv").to_dict()
        self.engine_frame = pd.read_csv("../data/raw/frame.csv").to_dict()
        self.alternator_fan = pd.read_csv("../data/raw/alternator_fan.csv").to_dict()
        self.electrical_ring = pd.read_csv("../data/raw/electrical_ring.csv").to_dict()
        self.alternator_skeleton = pd.read_csv("../data/raw/alternator_skeleton.csv").to_dict()


if __name__ == "__main__":
    costOpt = CostOptimizer('engine')
