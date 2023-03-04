
import pandas as pd
import numpy as np


TIO2_renaming = {
    "苯": "benzene",
    "甲苯": "toluene",
    "二甲苯": "xylene",
    "甲醛": "formaldehyde",
    "汽油": "gasoline",
    "柴油": "diesel_fuel",
    "H2": "h2",
    "CH4": "ch4"
}


metal_ox = "tio2"


def translateHeader(df):
    header = ['metal_ox', 'gas_cate', 'temperature', 'density', 'resp_density']
    # , 'metal', 'resp_val'
    df_header = list(df.head())
    for i in range(len(header)):
        df_header[i] = header[i]

    for i in range(len(df_header)):
        strsplit = df_header[i].split("+")
        if len(strsplit) > 1:
            df_header[i] = strsplit[1]
    # print(df_header)
    return df_header


def translateCasCate(df, sheetname):
    if sheetname in TIO2_renaming:
        # print(TIO2_renaming[sheetname])
        df['gas_cate'] = TIO2_renaming[sheetname]
    # print(df[:3])


def read_process(path):

    SheetNameDF = {}

    xl = pd.read_excel(path, None)

    sheetnames = xl.keys()

    dataframes = {}

    for k in sheetnames:
        curr_df = pd.read_excel(path, sheet_name=k)
        eng_header = translateHeader(curr_df)
        curr_df.columns = eng_header
        translateCasCate(curr_df, sheetname=k)
        # print(curr_df[:4])
        dataframes[TIO2_renaming[k]] = curr_df
    return dataframes


def sheet_dataset(df):
    dataset = []
    elements = list(df.head())

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

def removeBlankRespVal(df):
    
    df['resp_val'].replace('', np.nan, inplace=True)
    df.dropna(subset=['resp_val'], inplace=True)
    
def make_dataset(dfs):
    print("dfs size  ", len(dfs))

    dataset = []
    for d in dfs:
        sub_set = sheet_dataset(dfs[d])
        print(len(sub_set))
        dataset += sub_set
    print(len(dataset))
    print(dataset[:4])
    df = pd.DataFrame(dataset, columns=[
                      'metal_ox', 'gas_cate', 'temperature', 'density', 'resp_density', 'metal', 'resp_val'])
    print(df[:10])
    
    removeBlankRespVal(df)
    df.to_csv("dataset_in2o3_2.csv", index=False)


# path = "./files_需要转换成数据/TIO2.xlsx"
path = "./raw_data/in2o3.xlsx"


dfs = read_process(path=path)

for k in dfs:
    print(dfs[k][:4])
make_dataset(dfs)