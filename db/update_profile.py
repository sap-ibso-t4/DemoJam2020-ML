from db.sqliteAPI import SqliteAPI
from db.dict_to_itab import data_frame_to_internal_table
from scipy.stats import uniform


def update_profile(material_type):
    material_db = SqliteAPI('material.db')
    profile_db = SqliteAPI('profile.db')

    # get materail
    query = "select * from material where material_type = {}".format(material_type)
    mat_by_cat = data_frame_to_internal_table(material_db.dql_with_df(query))
    material_db.close()

    # set profile
    data_uniform = uniform.rvs(loc=0, scale=1000, size=len(mat_by_cat)).tolist()
    data_uniform = list(map(lambda x: round(x, 0), data_uniform))

    for i in range(len(mat_by_cat)):
        material_id = mat_by_cat[i]["material_id"]
        material_type = mat_by_cat[i]["material_type"]
        count = data_uniform[i]
        query = "insert or replace into user_profile(material_id, \
                 material_type, count) values ({}, {}, {})".format(
            material_id,
            material_type,
            count)
        profile_db.dml(query)
    profile_db.commit()
    profile_db.close()


if __name__ == "__main__":
    update_profile(1)
    update_profile(2)
    update_profile(3)
    update_profile(4)
    update_profile(5)
    update_profile(6)
    update_profile(7)
    update_profile(8)