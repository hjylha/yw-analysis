
import numpy as np
import pandas as pd

df = pd.read_csv("data/Daily m3 1315.csv")

s = list(df.columns).index("02/04/2012")
e = list(df.columns).index("20/04/2015")
cols = [0, 1, 2] + list(range(s, e + 1))
df = df.iloc[:, cols].dropna()

s1 = list(df.columns).index("09/09/2013")
e1 = list(df.columns).index("10/02/2015")
cols1 = [0, 1, 2] + list(range(s1, e1 + 1))
df1 = df.iloc[:, cols1].dropna()
df1 = df1[df["DMA"] == 1]
