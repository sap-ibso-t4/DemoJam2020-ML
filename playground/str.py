import random as rd
import pandas as pd


def random_pick(raw_data):
    return raw_data[rd.randrange(0, len(raw_data), 1)]


countries = ["USA", "Germany", "China", "Japan", "Brazil", "Canada", "France", "Italy", "Austria", "India",
             "Russia", "Mexico", "Belgium", "Norway", "New Zealand", "Netherlands", "Chile", "Cuba", "Denmark",
             "Romania", "Korea", "Egypt", "Switzerland", "Sweden", "Thailand", "Turkey", "Indonesia"]
firms = ["Volkswagen", "Ford", "Benz", "Daimler", "Mercedes", "BMW", "KTM", "Buick", "Acura", "Toyota", "Honda", "BYD",
         "GMC", "Hyundai", "Ferrari", "Jeep", "Lincoln", "Tesla", "Volvo"]

str = random_pick(firms) + " " + random_pick(countries) + " A" + str(rd.randrange(1000, 4000, 1))
print(str)
print(rd.uniform(450, 550))

PATH = '../data/raw/frame.csv'
df = pd.read_csv(PATH)
df["category description"] = df["category description"].replace("alternator", "frame")
df.to_csv(path_or_buf=PATH, sep=",", index=False)
