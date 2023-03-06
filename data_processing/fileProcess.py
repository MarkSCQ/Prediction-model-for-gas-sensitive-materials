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
    "CH4": "ch4",
    "WO3":"wo3"
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
    
    
    # df['gas_density'] = df['gas_density'].apply(lambda x: x[:-3])

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



def drop_zero_gas_density(df):
    # df.drop(df[df['Fee'] >= 24000].index, inplace = True)
    df.drop(df[df['gas_density'] == 0].index, inplace = True)    
    

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


def round_resp_val(df, filed="WO3", precision=1):
    print(df)
    # print(df["resp_val"])
    df[filed] = df[filed].round(precision)


def read_process(path, renaming_dict, metal):

    SheetNameDF = {}

    xl = pd.read_excel(path, None)

    sheetnames = xl.keys()

    dataframes = {}

    for k in sheetnames:
        if k in wo3_renaming:
            # renaming wo3 
            new_name = wo3_renaming[k]
            # read from excel file 
            curr_df = pd.read_excel(path, sheet_name=k)
            # get current header list
            curr_head = list(curr_df.head())
            # translate chi to eng
            translated = translate_column(curr_df, curr_head)
            # renaming header
            curr_df.columns = translated
            # fill nan blanks
            fill_blanks_df(curr_df, 0)
            # reshape the dataframes
            curr_df = columns_reshape(curr_df)  
            # remove rows when gas_density=0
            drop_zero_gas_density(curr_df)
            # add elements
            df_add_elements(curr_df, new_name, metal)
            # collect data
            dataframes[new_name] = curr_df
            global header
            header = list(curr_df.head())
            # round values
            round_resp_val(curr_df)
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
    # df['resp_density'] = df['resp_density'].str.rstrip('%').astype('float') / 100.0

    print(df[:10])

    df.to_csv("dataset_wo3.csv", index=False)



dataframes = read_process("../raw_data/wo3_mod.xlsx", wo3_renaming, metal_ox_wo3)
make_dataset(dataframes)
# dataframes
# df_add_elements()
# make_dataset_header()
