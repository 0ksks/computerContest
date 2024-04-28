import numpy as np
np.set_printoptions(precision=3)
import pandas as pd
pd.set_option('display.precision', 3)
from read_data import handle_cul_tra, handle_digital

def entropy_weight(df:pd.DataFrame)->pd.DataFrame:
    """
    熵权法计算权重

    Args:
        df (pd.DataFrame): 需要计算权重的数据

    Returns:
        pd.DataFrame: 熵权法权重
    """
    def entropy(x):
        x = np.where(x != 0, x, 1)
        return -np.sum(x * np.log(x))
    values = df.values.T
    normal = np.apply_along_axis(lambda x:(x - x.min())/(x.max() - x.min()), 1, values)
    partial = np.apply_along_axis(lambda x:x/sum(x), 1, normal)
    n = values.shape[1]
    columns = df.columns
    entropies = np.apply_along_axis(entropy, 1, partial)/np.log(n)
    redundancies = 1 - entropies
    weights = redundancies/sum(redundancies)
    data = np.stack([entropies, redundancies, weights])
    result = pd.DataFrame(data, columns=columns, index="信息熵值e 信息效用值d 权重系数w".split())
    return result

def combine(df:pd.DataFrame, name:str=None)->pd.DataFrame:
    """
    根据熵权法计算的权重合并数据

    Args:
        df (pd.DataFrame): 需要合并的数据
        name (str, optional): 合并后的数据名称. Defaults to None.

    Returns:
        pd.DataFrame: 合并后的数据
    """
    weights = entropy_weight(df).loc["权重系数w"].values
    normal = np.apply_along_axis(lambda x:(x - x.min())/(x.max() - x.min()), 0, df.values)
    weightedValues = np.apply_along_axis(lambda x: sum(np.multiply(weights,x)), 1, normal)
    name = name if name else "combined"
    resultDF = pd.DataFrame(data=weightedValues.reshape((-1,1)), columns=[name,], index=df.index)
    return resultDF

if __name__ == "__main__":
    df = handle_digital()
    result = combine(df)
    print(result)
    