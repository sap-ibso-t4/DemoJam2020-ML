def data_frame_to_internal_table(df):
    '''
    This is trying to simulate internal table in ABAP
    Using array as table and diction as structure
    :param dict:
    :return: itab(list)
    '''
    dict = df.to_dict()
    keys = list(dict.keys())
    # try to get row number
    values = list(dict.values())
    if len(values) == 0:
        return  # empty dictionary
    else:
        row_number = len(values[0])

    itab = []
    for i in range(row_number):
        line = {}
        for j in range(len(keys)):
            line[keys[j]] = values[j][i]
        itab.append(line)
    return itab


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('../csvData/raw/engine.csv')
    itab = data_frame_to_internal_table(df)
    print(itab[0])
