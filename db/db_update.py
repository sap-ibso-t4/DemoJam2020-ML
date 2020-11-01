from db.sqliteAPI import SqliteAPI
import pandas as pd
import random as rd
import datetime

db = SqliteAPI('material.db')


def random_pick(raw_data):
    return raw_data[rd.randrange(0, len(raw_data), 1)]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = rd.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)


def update_material():
    # get current material ID
    count = db.dql('dql material_id from material order by material_id desc limit 1')
    init_material_id = 0
    for row in count:
        init_material_id = row[0]
    print(init_material_id)

    # engine
    df = pd.read_csv('../csvData/raw/pistons.csv')
    df["material ID"] = df["material ID"].add(init_material_id)
    # handle line one by one
    for i in range(df.shape[0]):
        rd_date = random_date(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))
        s = df.iloc[i]
        query = "insert into material (material_id,material_group,\
                 material_type,group_desc,type_desc,material_desc,ref_type,\
                 gross_weight,net_weight,weight_unit,volumn,volumn_unit,length,width,\
                 height,uom,create_time,price,currency,rank)\
                 values ({},{},{},'{}','{}','{}',{},{},{},'{}',{},'{}',{},{},{},'{}','{}',{},'{}',{})".format(
            s["material ID"],
            1,
            s["category"],
            'engine',
            s["category description"],
            s["description"],
            1,
            round(rd.uniform(2, 5), 2),
            round(rd.uniform(1, 3), 2),
            s["weight uom"],
            round(s["bore"] * s["stroke"] * s["bore"], 2),
            s["size uom"],
            s["bore"],
            s["stroke"],
            s["bore"],
            s["size uom"],
            rd_date,
            s["price"],
            s["currency"],
            s["rank"])
        # query = "insert into material (material_id,material_group,\
        #     material_type,group_desc,type_desc,material_desc,ref_type,\
        #     gross_weight,net_weight,weight_unit,volumn,volumn_unit,length,width,\
        #     height,uom,create_time,price,currency,rank)\
        #     values ({},{},{},'{}','{}','{}','',{},{},'KG',{},'CM',{},{},{},'CM','{}',{},'EUR',{})".format(
        #     s["material ID"],
        #     s["category"],
        #     s["category"],
        #     s["category description"],
        #     s["category description"],
        #     s["description"],
        #     round(rd.uniform(120, 170), 2),
        #     round(rd.uniform(100, 150), 2),
        #     round(s["length"] * s["width"] * s["height"], 2),
        #     s["length"],
        #     s["width"],
        #     s["height"],
        #     rd_date,
        #     s["price"],
        #     s["rank"])

        print(query)
        db.dml(query)
        db.commit()


def update_vendor():
    def get_vendor_id(firm, country, list):
        for i in range(len(list)):
            if (firm, country) == list[i]:
                return i + 1

    data = db.dql('dql * from material')
    check_list = []

    for row in data:
        if row[6] != 0:
            str_split = row[5].split(" ")
            firm = str_split[0]
            country = str_split[1]
            check_tuple = (firm, country)
            if check_tuple not in check_list:
                check_list.append(check_tuple)
            if row[0] % 7 != 0:
                query = "insert into vendor (material_id, vendor, vendor_description, country) \
                        values({},{},'{}','{}')".format(
                    row[0],
                    get_vendor_id(firm, country, check_list),
                    firm + " " + country + " Broker",
                    country)
                db.dml(query)
                db.commit()
        else:
            query = "insert into vendor (material_id, vendor, vendor_description, country) \
                                    values({},{},'{}','{}')".format(
                row[0],
                0,
                'Central Engine Broker',
                'China')
            db.dml(query)
            db.commit()


def update_plant():
    def get_plant_id(firm, country, list):
        for i in range(len(list)):
            if (firm, country) == list[i]:
                return i + 1

    data = db.dql('dql * from material where material_type <> 1')
    check_list = []

    for row in data:
        str_split = row[5].split(" ")
        firm = str_split[0]
        country = str_split[1]
        check_tuple = (firm, country)
        if check_tuple not in check_list:
            check_list.append(check_tuple)
        if row[0] % 7 == 0 and row[6] == 1:
            query = "insert into plant (material_id, plant, plant_description, country) \
                    values({},{},'{}','{}')".format(
                row[0],
                get_plant_id(firm, country, check_list),
                firm + " " + country + " Factory",
                country)
            db.dml(query)
            db.commit()


if __name__ == "__main__":
    # update_material()
    # update_plant()
    update_vendor()
    db.close()
    # print(random_date(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)))
