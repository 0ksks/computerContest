import pandas as pd
from read_data import handle_digital, handle_cul_tra, handle_control
from weight import combine
from biselect import select
import os
import statsmodels.api as sm

digital = handle_digital()
digitalIndex = combine(digital, "数字化指标")

culTra = handle_cul_tra()
culTraIndex = combine(culTra, "文旅指标")

control = handle_control()

combined = pd.concat([control, digitalIndex, culTraIndex], axis=1).astype(float)

def save_LR(X, y, path, name):
    """
    进行一次线性回归

    Args:
        X (pd.Dataframe): 解释变量
        y (pd.Dataframe): 被解释变量
        path (str): 结果保存文件路径
        name (str): 结果保存文件名
    """
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}/{name}.txt","w") as f:
        f.write(str(sm.OLS(y, sm.add_constant(X)).fit().summary()))
if __name__ == "__main__":
    df = pd.concat([control,digitalIndex,culTraIndex],axis=1).astype(float)
    for cols in select(control.columns):
        save_LR(df[cols+["数字化指标"]],df["文旅指标"],"res","_".join(cols))