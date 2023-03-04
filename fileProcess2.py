
import pandas as pd


TIO2_renaming = {
    "苯": "benzene",
    "甲苯": "toluene",
    "二甲苯": "xylene",
    "甲醛": "formaldehyde",
    "汽油": "gasoline",
    "柴油": "diesel_fuel",
    "H2":"h2",
    "CH4":"ch4"
}



metal_ox = "tio2"


def translateHeader(df):
    header = ['metal_ox', 'gas_cate', 'temperature', 'density', 'resp_density']
    # , 'metal', 'resp_val'
    df_header = list(df.head())
    for i in range(len(header)):
        df_header[i]=header[i]
    
    for i in range(len(df_header)):
        strsplit = df_header[i].split("+")
        if len(strsplit)>1:
            df_header[i]=strsplit[1]
    # print(df_header)
    return df_header


def translateCasCate(df,sheetname):
    if sheetname in TIO2_renaming:
        # print(TIO2_renaming[sheetname])
        df['gas_cate']=TIO2_renaming[sheetname]
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
        print(curr_df[:4])

    return dataframes


path = "./files_需要转换成数据/TIO2.xlsx"


read_process(path=path)

