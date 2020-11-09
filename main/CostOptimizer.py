from db import SqliteAPI, data_frame_to_internal_table
from main.CategoryItemOptimizer import CategoryItemOptimizer
import numpy as np
from scipy.sparse.csgraph import shortest_path
from scipy.sparse import csr_matrix
import random as rd


class CostOptimizer:
    """
    Cost optimizer for mbom
    """

    def __init__(self, material_group):
        self.INIT_EDGE = .1  # very minor constant for edge
        self.material_group = material_group
        self.material_types = self.__get_all_category_related_material_type()
        self.tree = self.__random_generate_tree()

    def __get_all_category_related_material_type(self):
        """
        Get all materials refer to ebom
        :return:
        """
        material_db = SqliteAPI('../db/material.db')
        query = "select material_type from material where material_group = {} \
                 group by material_type".format(
            self.material_group
        )
        material_type_internal_table = data_frame_to_internal_table(material_db.dql_with_df(query))
        material_db.close()
        return material_type_internal_table

    def __get_suggested_all_materials(self):
        """
        This method call item optimizer to get suggested material by each material type
        :return:
        """
        materials = []
        for line in self.material_types:
            material = CategoryItemOptimizer(line["material_type"]).process()
            materials.append(material)
        return materials

    def __set_graphic_indice(self, material_list):
        """
        Set graphic position list
        :param material_list:
        :return: list
        """
        material_hierarchies = list()

        for line in material_list:
            material_hierarchy = {
                "material_id": line["material_id"],
                "material_type": line["material_type"],
                "price": line["price"]
            }
            ref_materials = list()
            for material in material_list:
                if material["ref_type"] == material_hierarchy["material_type"]:
                    ref_material_line = {
                        "material_id": material["material_id"],
                        "material_type": material["material_type"],
                        "price": material["price"]
                    }
                    ref_materials.append(ref_material_line.copy())
            material_hierarchy["ref_mat"] = ref_materials
            material_hierarchies.append(material_hierarchy.copy())

            # for graph perspective, we need to insert initial node at beginning place
        material_hierarchies.insert(0, {
            "material_id": 0,
            "material_type": 0,
            "price": 0,
            "ref_mat": []
        })
        print(material_hierarchies)

    def __build_graph(self):
        """
        build adjacency matrix
        :param material_list:
        :return: nd.array as graph
        """
        # build graph skeleton
        # adjacency_matrix = np.zeros(
        #     (len(material_list) + 1, len(material_list) + 1))  # one more node for initial vertices
        # self.__set_graphic_indice(material_list)
        adjacency_matrix = np.array([
            [0, 3474.87, 210.78, 0, 0, 0, 127.09, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 319.31, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 568.57, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 55070.72, 0, 0, 0],
            [0, self.INIT_EDGE, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 20.28, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 277.33],
            [0, 0, self.INIT_EDGE, 0, 0, 0, 0, 0, 0]
        ])
        graph = csr_matrix(adjacency_matrix)
        d, pr = shortest_path(graph, directed=False, method='D', return_predecessors=True)
        return d, pr

    def __build_tree_layer(self, current_layer_id, material_internal_table):
        db = SqliteAPI('../db/material.db')
        plant = db.dql_with_df('select * from plant')
        plant.set_index("material_id")
        vendor = db.dql_with_df('select * from vendor')
        vendor.set_index("material_id")
        db.close()

        current_layer_id = current_layer_id + 1
        layer = []
        for i in range(rd.randint(2, 3)):
            random_nr = rd.randint(0, len(material_internal_table) - 1)

            try:
                plant_id = plant["plant_description"][
                    plant.index.get_loc(material_internal_table[random_nr]["material_id"])]
            except KeyError:
                plant_id = ""

            try:
                vendor_id = vendor["vendor_description"][
                    vendor.index.get_loc(material_internal_table[random_nr]["material_id"])]
            except KeyError:
                vendor_id = ""

            node = {
                "text": "Material ID: {}/{}".format(
                    material_internal_table[random_nr]["material_id"],
                    material_internal_table[random_nr]["material_desc"]),
                "ref": "",
                "gross_weight": material_internal_table[random_nr]["gross_weight"],
                "net_weight": material_internal_table[random_nr]["net_weight"],
                "weight_unit": material_internal_table[random_nr]["weight_unit"],
                "volume": material_internal_table[random_nr]["volumn"],
                "volume_unit": material_internal_table[random_nr]["volumn_unit"],
                "length": material_internal_table[random_nr]["length"],
                "width": material_internal_table[random_nr]["width"],
                "height": material_internal_table[random_nr]["height"],
                "uom": material_internal_table[random_nr]["uom"],
                "price": material_internal_table[random_nr]["price"],
                "plant": plant_id,
                "vendor": vendor_id,
                "currency": material_internal_table[random_nr]["currency"],
                "rank": material_internal_table[random_nr]["rank"]
            }
            rd_choice = rd.choice([True, False])
            if rd_choice and current_layer_id <= 3:
                node["nodes"] = self.__build_tree_layer(current_layer_id, material_internal_table)
            layer.append(node.copy())
        return layer

    def __random_generate_tree(self):
        mat_db = SqliteAPI('../db/material.db')
        query = "select * from material"
        mat_int = data_frame_to_internal_table(mat_db.dql_with_df(query))
        mat_db.close()

        # init root node
        number_of_root = 5
        tree = []
        for i in range(number_of_root):
            for line in self.__build_tree_layer(0, mat_int):
                tree.append(line)
        return tree

    def get_tree(self):
        return self.tree

    def get_expand_tree(self):
        # mat_db = SqliteAPI('../db/material.db')
        # query = "select * from material"
        # mat_int = data_frame_to_internal_table(mat_db.dql_with_df(query))
        # mat_db.close()
        #
        # self.tree[0] = self.__build_tree_layer(0, mat_int)
        print(self.tree[0])

    def process(self):
        """
        main processor
        :return: best route of materials(dict)
        """
        materials = self.__get_suggested_all_materials()
        D, Pr = self.__build_graph(materials)
        return Pr


if __name__ == "__main__":
    costOpt = CostOptimizer(1)
    print(costOpt.get_tree())
