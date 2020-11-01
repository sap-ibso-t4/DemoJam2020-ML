import numpy as np
from db import SqliteAPI, data_frame_to_internal_table
from main.CategoryItemOptimizer import CategoryItemOptimizer


class CostOptimizer:
    """
    Cost optimizer for mbom
    """

    def __init__(self, category_key):
        self.category_key = category_key
        self.material_types = self.__get_all_category_related_material_type()
        self.materials = []

    def __get_all_category_related_material_type(self):
        material_db = SqliteAPI('../db/material.db')
        query = "select material_type from material where ref_type = {} \
                 group by material_type".format(
            self.category_key
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

    def process(self):
        self.materials = self.__get_optimized_materials()
        print(self.materials)
        print(len(self.materials))


if __name__ == "__main__":
    costOpt = CostOptimizer(2)
    costOpt.process()
