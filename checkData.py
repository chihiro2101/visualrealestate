



# link visualize data
# https://colab.research.google.com/drive/1J4FrbZ9lpRp87hK2hfYc0Wyu1B9d8SqF?usp=sharing

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')
import random
import math

# df = pd.read_csv("dfBDS.csv", dtype = {"id":"string", "month": "string"})
df = pd.read_csv("dfBDS.csv")
percentage_of_null = df.isnull().sum() * 100 / len(df)
print(percentage_of_null)

#Loại bỏ thuộc tính có giá trị NaN > 60%
newdf = df.drop('law_doc', axis=1)

#Loại bỏ các bản ghi không có giá hoặc giá không xác định
newdf = newdf[newdf['price'].notnull()]
newdf = newdf.loc[(newdf['price'] != 'Thỏa thuận')]
newdf['price'] = newdf['price'].apply(lambda x : float(x))
newdf = newdf.loc[(newdf['price'] < 10000)]

newdf = newdf.loc[(newdf['square'] < 500)]
newdf = newdf.loc[(newdf['bedrooms'] < 5)]
newdf = newdf.loc[(newdf['bathrooms'] < 5)]
newdf = newdf[newdf['district'].notnull()]
newdf.to_csv (r'newdfBDS.csv', index = False, header=True)
print("DONE")