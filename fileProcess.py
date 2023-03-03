import pandas as pd
# import numpy as np

wo3_renaming = {
    "苯": "benzene",
    "甲苯": "toluene",
    "二甲苯": "xylene",
    "甲醛": "formaldehyde",
    "汽油": "gasoline",
    "柴油": "diesel_fuel"
}

metal_ox_wo3 = "wo3"
# 苯 benzene
# 甲苯 toluene
# 二甲苯 Xylene
# 甲醛 formaldehyde
# 汽油 gasoline
# 柴油 diesel fuel


def translate_column(df,headnames):

    
    headnames = list(map(lambda x: x.replace(headnames[0], 'density_temp'), headnames))
    headnames = list(map(lambda x: x.replace(headnames[1], 'gas_density'), headnames))
    
    for idx in range(len(headnames)):
        # nsp = 
        element_pairs = headnames[idx].split("#")
        if len(element_pairs)>1:
            headnames[idx]=element_pairs[1] 
    
    return headnames

def columns_reshape(df):
    df =  df.copy()

    df[['density','temperature']] = df.density_temp.str.split(",",expand=True)
    df = df.drop(['density_temp'], axis=1)
    df['gas_density'] = df['gas_density'].apply(lambda x:x[:-3])

    df['density']=df['density'].apply(lambda x:x[:-3])
    df['temperature']=df['temperature'].apply(lambda x:x[:-1])

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
        curr_cell =df.iloc[r,col]
        if not pd.isna(curr_cell):
            # currflag = "250℃"
            curr_val = curr_cell
            # df.iloc[r,col]=curr_val
        else:
            # if nan, set val
            df.iloc[r,col]=curr_val
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
            
            translated = translate_column(curr_df,curr_head)
            curr_df.columns = translated
            
            fill_blanks_df(curr_df, 0)
            curr_df=columns_reshape(curr_df)
            df_add_elements(curr_df, new_name, metal)

            dataframes[new_name] = curr_df
    return dataframes


def make_dataset(dfs):
    print("dfs size  ",len(dfs))
    for d in dfs:
        print(dfs[d][:5])
    pass

# read dataframes
# def readXlsx(path, renaming_dict, gas, metal):

dataframes = read_process("./files_未调整格式/WO3.xlsx", wo3_renaming,metal_ox_wo3)
make_dataset(dataframes)
# dataframes
# df_add_elements()
