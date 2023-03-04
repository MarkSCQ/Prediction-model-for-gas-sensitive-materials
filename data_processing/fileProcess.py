import pandas as pd
# import numpy as np

wo3_renaming = {
    "苯": "benzene",
    "甲苯": "toluene",
    "二甲苯": "xylene",
    "甲醛": "formaldehyde",
    "汽油": "gasoline",
    "柴油": "diesel_fuel",
    "H2": "h2",
    "CH4": "ch4"
}

metal_ox_wo3 = "wo3"
# 苯 benzene
# 甲苯 toluene
# 二甲苯 Xylene
# 甲醛 formaldehyde
# 汽油 gasoline
# 柴油 diesel fuel

# header=[]


def translate_column(df, headnames):

    headnames = list(map(lambda x: x.replace(
        headnames[0], 'density_temp'), headnames))
    headnames = list(map(lambda x: x.replace(
        headnames[1], 'gas_density'), headnames))

    for idx in range(len(headnames)):
        # nsp =
        element_pairs = headnames[idx].split("#")
        if len(element_pairs) > 1:
            headnames[idx] = element_pairs[1]

    return headnames


def columns_reshape(df):
    df = df.copy()

    df[['density', 'temperature']] = df.density_temp.str.split(
        ",", expand=True)
    df = df.drop(['density_temp'], axis=1)
    df['gas_density'] = df['gas_density'].apply(lambda x: x[:-3])

    df['density'] = df['density'].apply(lambda x: x[:-3])
    df['temperature'] = df['temperature'].apply(lambda x: x[:-1])

    header = df.columns.tolist()
    header.insert(0, header[-1])
    header.insert(0, header[-2])
    header.pop()
    header.pop()
    df = df[header]
    return df
    # return target


def fill_blanks_df(df, col):
    curr_val = 0
    for r in range(len(df)):
        # if not nan, update mod_val
        curr_cell = df.iloc[r, col]
        if not pd.isna(curr_cell):
            # currflag = "250℃"
            curr_val = curr_cell
            # df.iloc[r,col]=curr_val
        else:
            # if nan, set val
            df.iloc[r, col] = curr_val
    return df

# def fill_blanks(df_list):
#     d_list = []
#     for d in df_list:
#         d_list.append(fill_blanks_df(df,0))

#     return d_list


def add_gas(df, gas=""):
    df.insert(0, 'gas_cate', gas)


def add_metal_ox(df, metal=""):
    df.insert(0, 'metal_ox', metal)


def df_add_elements(df, gas, metal):
    add_gas(df, gas)
    add_metal_ox(df, metal)


def renaming_title(df):
    curr_df_header = list(df.head())


def read_process(path, renaming_dict, metal):

    SheetNameDF = {}

    xl = pd.read_excel(path, None)

    sheetnames = xl.keys()

    dataframes = {}

    for k in sheetnames:
        if k in wo3_renaming:
            new_name = wo3_renaming[k]
            curr_df = pd.read_excel(path, sheet_name=k)

            curr_head = list(curr_df.head())

            translated = translate_column(curr_df, curr_head)
            curr_df.columns = translated

            fill_blanks_df(curr_df, 0)
            curr_df = columns_reshape(curr_df)
            df_add_elements(curr_df, new_name, metal)

            dataframes[new_name] = curr_df
            global header
            header = list(curr_df.head())
            # print(header)

    return dataframes


def make_dataset_header():
    curr_header = header[:5]
    curr_header.insert(2, "element")
    curr_header.append("resp_val")
    return curr_header


def sheet_dataset(df):
    dataset = []
    elements = list(df.head())
    print(elements)
    for row in range(len(df)):
        data = list(df.iloc[row])
        tmp = data[0:5]
        for col in range(5, len(data)):
            tmp.append(elements[col])

            tmp.append(data[col])
            dataset.append(tmp)
            tmp = data[0:5]
    print(dataset[:3])
    return dataset


def make_dataset(dfs):
    print("dfs size  ", len(dfs))

    # ds_header = make_dataset_header()
    dataset = []
    for d in dfs:
        sub_set = sheet_dataset(dfs[d])
        print(len(sub_set))
        dataset += sub_set
    print(len(dataset))
    print(dataset[:4])
    df = pd.DataFrame(dataset, columns=[
                      'metal_ox', 'gas_cate', 'temperature', 'density', 'resp_density', 'metal', 'resp_val'])
    # df["resp_density"] = pd.to_numeric(df["resp_density"])
    df['resp_density'] = df['resp_density'].str.rstrip('%').astype('float') / 100.0

    print(df[:10])
    df.to_csv("dataset_wo3.csv", index=False)



dataframes = read_process("./files_未调整格式/WO3.xlsx", wo3_renaming, metal_ox_wo3)

make_dataset(dataframes)
# dataframes
# df_add_elements()
# make_dataset_header()
