from db import SqliteAPI, data_frame_to_internal_table
import numpy as np


class CategoryItemOptimizer(object):
    """
    For each category level pick one suggested material
    """

    def __init__(self, material_type):
        """
        constructor
        :param material_type:
        """
        self.material_type = material_type
        self.raw_material = self.__load_material()

    def __load_material(self):
        """
        Load material from db
        :return: material internal table
        """
        data_db = SqliteAPI('../db/material.db')
        query = "select * from material where material_type = {}".format(
            self.material_type
        )
        material_internal_table = data_frame_to_internal_table(data_db.dql_with_df(query))
        data_db.close()
        return material_internal_table

    @staticmethod
    def __cosine(data_a, data_b):
        """
        cosine get closest
        :param data_a: ndarray
        :param data_b: ndarray
        :return: score
        """
        sum_data = data_a.T.dot(data_b)
        denom = np.linalg.norm(data_a) * np.linalg.norm(data_b)
        return 0.5 + 0.5 * (sum_data / denom)

    def __item_CF(self):
        """
        item based cross filter
        :return: closest material
        """
        # item based cross filter
        # get user profile
        user_profile = self.__get_user_profile()
        if user_profile is not None:
            user_profile_array = []
            for line in user_profile:
                count = line["count"]
                user_profile_array.append(count)

            user_profile = np.array(user_profile_array)

            # pick item profile
            item_profile_array = []
            for line in self.raw_material:
                gross_weight = line["gross_weight"]
                net_weight = line["net_weight"]
                volume = line["volumn"]
                length = line["length"]
                width = line["width"]
                height = line["height"]
                price = line["price"]
                rank = line["rank"]
                item_profile_line = [gross_weight, net_weight, volume, length, width, height, price, rank]
                item_profile_array.append(item_profile_line)

            item_profile = np.array(item_profile_array)

            # get user feature
            user_prefer_feature = user_profile.dot(item_profile)  # shape(1, 8)

            # get closest material
            scored_list = []
            for i in range(len(item_profile)):
                score = self.__cosine(user_prefer_feature, item_profile[i])
                scored_item = {
                    "score": score,
                    "index": i
                }
                scored_list.append(scored_item)

            biggest_score = 0
            material_index = 0
            for i in range(len(scored_list)):
                if biggest_score < scored_list[i]["score"]:
                    biggest_score = scored_list[i]["score"]
                    material_index = scored_list[i]["index"]
        else:
            # using customized weight to get optimized material
            # here using price
            lowest_weight = 0
            material_index = 0
            for i in range(len(self.raw_material)):
                if lowest_weight > self.__get_customized_weight(self.raw_material[i]):
                    lowest_weight = self.__get_customized_weight(self.raw_material[i])
                    material_index = i

        return material_index

    @staticmethod
    def __get_customized_weight(line_of_material):
        """
        fake method for weight
        :param line_of_material:
        :return: weight
        """
        weight = line_of_material["price"]
        return weight

    def __get_user_profile(self):
        """
        Get user profile from profile db
        :return: user profile internal table
        """
        profile_db = SqliteAPI('../db/profile.db')
        query = "select count from user_profile where material_type = {}".format(
            self.material_type
        )
        profile_internal_table = data_frame_to_internal_table(profile_db.dql_with_df(query))
        profile_db.close()
        return profile_internal_table

    def process(self):
        """
        main process method
        :return: closest material
        """
        index = self.__item_CF()
        material = self.raw_material[index]
        return material


if __name__ == "__main__":
    flt = CategoryItemOptimizer(6)
    print(flt.process())
