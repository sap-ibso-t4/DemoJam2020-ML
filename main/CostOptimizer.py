from db import SqliteAPI, data_frame_to_internal_table
from main.CategoryItemOptimizer import CategoryItemOptimizer
import numpy as np


class CostOptimizer:
    """
    Cost optimizer for mbom
    """

    def __init__(self, material_group):
        self.INIT_EDGE = .1  # very minor constant for edge
        self.material_group = material_group
        self.material_types = self.__get_all_category_related_material_type()

    def __get_all_category_related_material_type(self):
        material_db = SqliteAPI('../db/material.db')
        query = "select material_type from material where material_group = {} \
                 group by material_type".format(
            self.material_group
        )
        material_type_internal_table = data_frame_to_internal_table(material_db.dql_with_df(query))
        material_db.close()
        return material_type_internal_table

    def __get_optimized_materials(self):
        materials = []
        for line in self.material_types:
            material = CategoryItemOptimizer(line["material_type"]).process()
            materials.append(material)
        return materials

    def __build_graph(self, material_list):
        """
        build adjacency matrix
        :param material_list:
        :return: nd.array as graph
        """
        # build graph skeleton
        adjacency_matrix = np.zeros(
            (len(material_list) + 1, len(material_list) + 1))  # one more node for initial vertices
        print(adjacency_matrix)

    def process(self):
        materials = self.__get_optimized_materials()
        self.__build_graph(materials)


if __name__ == "__main__":
    costOpt = CostOptimizer(1)
    costOpt.process()
