import pandas as pd
import random as rd


def random_pick(raw_data):
    return raw_data[rd.randrange(0, len(raw_data), 1)]


def build_csv(PATH):
    # define dimension
    rawData = dict()
    # alternator
    mid = 0
    countries = ["USA", "Germany", "China", "Japan", "Brazil", "Canada", "France", "Italy", "Austria", "India",
                 "Russia", "Mexico", "Belgium", "Norway", "New Zealand", "Netherlands", "Chile", "Cuba", "Denmark",
                 "Romania", "Korea", "Egypt", "Switzerland", "Sweden", "Thailand", "Turkey", "Indonesia"]
    firms = ["Volkswagen", "Ford", "Benz", "Daimler", "Mercedes", "BMW", "KTM", "Buick", "Acura", "Toyota", "Honda",
             "BYD", "GMC", "Hyundai", "Ferrari", "Jeep", "Lincoln", "Tesla", "Volvo"]
    rawData = {
        "material ID": [],
        "description": [],
        "level": [],
        "category": [],
        "category description": [],
        "hierarchy category": [],
        "provider": [],
        "country": [],
        # "length": [],
        # "height": [],
        # "bore": [],  # 缸径
        # "bore type": [],
        # "bore type description": [],
        # "stroke": [],  # 冲程
        # "stroke type": [],
        # "stroke type description": [],
        "diameter": [],
        "width": [],
        "size uom": [],
        "weight": [],
        "weight uom": [],
        # "power": [],
        # "voltage": [],
        # "current": [],  # 电流
        # "pressure": [],
        # "flow": [],  # 流量
        # "frequency": [],
        # "rotation speed": [],
        "price": [],
        "currency": [],
        "rank": [],
        "is leaf": []
    }

    for key, value in rawData.items():
        for i in range(10000):
            if key == "material ID":
                mid += 1
                value.append(mid)
            elif key == "description":
                string = random_pick(firms) + " " + random_pick(countries) + " R" + str(rd.randrange(1000, 40000, 1))
                value.append(string)
            elif key == "level":
                value.append(3)
            elif key == "category":
                value.append(7)
            elif key == "category description":
                value.append("electrical ring")
            elif key == "hierarchy category":
                value.append(2)
            elif key == "provider":
                desc = rawData["description"][i]
                keys = desc.split(" ")
                value.append(keys[0])
            elif key == "country":
                desc = rawData["description"][i]
                keys = desc.split(" ")
                value.append(keys[1])
            elif key == "diameter":
                value.append(round(rd.uniform(300, 500), 0))
            # elif key == "length":
            #     value.append(round(rd.uniform(550, 600), 2))
            # elif key == "height":
            #     value.append(round(rd.uniform(350, 450), 2))
            # elif key == "bore":
            #     value.append(round(rd.uniform(70, 120), 0))
            # elif key == "bore type":
            #     bore = rawData["bore"][i]
            #     if bore <= 95:
            #         value.append(1)
            #     else:
            #         value.append(2)
            # elif key == "bore type description":
            #     bore_type = rawData["bore type"][i]
            #     if bore_type == 1:
            #         value.append("big")
            #     elif bore_type == 2:
            #         value.append("small")
            # elif key == "stroke":
            #     value.append(round(rd.uniform(85, 140), 0))
            # elif key == "stroke type":
            #     stroke = rawData["stroke"][i]
            #     if stroke <= 100:
            #         value.append(1)
            #     else:
            #         value.append(2)
            # elif key == "stroke type description":
            #     stroke_type = rawData["stroke type"][i]
            #     if stroke_type == 1:
            #         value.append("short")
            #     elif stroke_type == 2:
            #         value.append("long")
            elif key == "width":
                value.append(round(rd.uniform(5, 7), 2))
            elif key == "size uom":
                value.append("mm")
            elif key == "weight":
                value.append(round(rd.uniform(0.2, 1), 2))
            elif key == "weight uom":
                value.append("kg")
            # elif key == "power":
            #     value.append(random_pick([24, 36]))
            # elif key == "voltage":
            #     value.append(12)
            # elif key == "current":
            #     value.append(random_pick([2.5, 3]))
            # elif key == "pressure":
            #     value.append(300)
            # elif key == "flow":
            #     value.append(random_pick([45, 50, 55, 65, 70, 75, 80, 85]))
            # elif key == "frequency":
            #     value.append(50)
            # elif key == "rotation speed":
            #     value.append(6000)
            elif key == "price":
                value.append(round(rd.uniform(10, 25), 2))
            elif key == "currency":
                value.append("eur")
            elif key == "rank":
                value.append(round(rd.uniform(6, 10), 0) / 2)
            elif key == "is leaf":
                value.append(True)

    for key, value in rawData.items():
        print(key, len(value))

    df = pd.DataFrame(rawData)
    df.to_csv(path_or_buf=PATH, sep=",", index=False)


build_csv("../csvData/raw/electrical_ring.csv")
