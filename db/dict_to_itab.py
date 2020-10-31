def data_frame_to_internal_table(data_frame):
    """
    This is trying to simulate internal table in ABAP
    Using array as table and diction as structure
    :param dict:
    :return: internal_table(list)
    """
    convertible_diction = data_frame.to_dict()
    keys = list(convertible_diction.keys())
    # try to get row number
    values = list(convertible_diction.values())
    if len(values) == 0:
        return  # empty dictionary
    else:
        row_number = len(values[0])

    internal_table = []
    for i in range(row_number):
        line = {}
        for j in range(len(keys)):
            line[keys[j]] = values[j][i]
        internal_table.append(line)
    return internal_table


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('../csvData/raw/engine.csv')
    internal_table = data_frame_to_internal_table(df)
    print(internal_table[0])
