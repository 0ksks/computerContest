"""
数据处理（清洗）代码
"""
import pandas as pd
import numpy as np

def clean_one(df:pd.DataFrame)->np.ndarray:
    df = df[df["地区"]=="全国"]
    df = df.drop("地区 指标 频度 单位".split(), axis=1).T
    df.index = map(int, df.index)
    values = df.loc[2013:2022].values
    return values.reshape(-1)

def handle_control()->pd.DataFrame:
    """
    处理控制变量
    """
    control = pd.read_excel("data/控制变量.xlsx", sheet_name=None)
    
    educationExpenditure = control["教育经费"]
    educationExpenditure = clean_one(educationExpenditure)
    
    GDP = control["GDP"]
    GDP = clean_one(GDP)

    CPI = control["居民消费价格指数"]
    CPI = CPI.iloc[-1].dropna()
    CPI.index = map(int, CPI.index)
    CPI = CPI.loc[2013:2022].values

    trafficStream = control["客运量"]["客运量自总计/万人"].values

    resultData = np.stack([educationExpenditure, GDP, CPI, trafficStream]).T
    result = pd.DataFrame(resultData, columns="教育经费 GDP CPI 客运量".split(), index=range(2013, 2023))
    return result

def handle_digital()->pd.DataFrame:
    """
    处理数字化相关变量
    """
    df:pd.DataFrame = pd.read_excel("data/数字化.xlsx").bfill()
    df = df.set_index("年份").rename_axis(None)
    return df

def handle_cul_tra()->pd.DataFrame:
    """
    处理文旅相关变量
    """
    culTra = pd.read_excel("data/文旅.xlsx", sheet_name=None)
    
    nationNature = clean_one(culTra["国家级自然保护区"])
    nationNature[-1] = nationNature[-2]
    
    library = culTra["县域图书馆"].iloc[:,1].values
    
    culSt = culTra["乡村文化站"].iloc[:,1].values
    
    travelIncomeCustomer = culTra["乡村旅游收入及人数"].ffill()
    travelIncome = travelIncomeCustomer.iloc[:,1].values
    travelCustomer = travelIncomeCustomer.iloc[:,2].values
    
    resultData = np.stack([nationNature, library, culSt, travelIncome, travelCustomer]).T
    result = pd.DataFrame(resultData, columns="国家级自然保护区 县域图书馆 乡村文化站 乡村旅游收入 乡村旅游人数".split(), index=range(2013, 2023))

    return result

if __name__ == "__main__":
    handle_cul_tra()
