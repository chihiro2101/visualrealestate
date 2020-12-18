import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')
import random
import math

df = pd.read_csv("dfBDS.csv", dtype = {"month": "string"})
df['id'] = df['id'].apply(lambda x : str(x).split('.')[0])
percentage_of_null = df.isnull().sum() * 100 / len(df)
print(percentage_of_null)
newdf = df.drop('law_doc', axis=1)
sample = newdf.head(100)


#1, bieu do the hien so luong bai dang theo thang
month_df = newdf[newdf['month'].notnull()]
# month_df = month_df.sort_values(by = 'month')
month = month_df.groupby(by = 'month').size().reset_index(name='counts')

# fig, ax = plt.subplots(figsize=(12, 7), subplot_kw=dict(aspect="equal"), dpi= 80)

# data = month['counts']
# categories = month['month']
# explode = [0,0,0,0,0,0.1,0,0,0,0]

# def func(pct, allvals):
#     absolute = int(pct/100.*np.sum(allvals))
#     return "{:.1f}% ({:d} )".format(pct, absolute)

# wedges, texts, autotexts = ax.pie(data, 
#                                   autopct=lambda pct: func(pct, data),
#                                   textprops=dict(color="w"), 
#                                   colors=plt.cm.Dark2.colors,
#                                  startangle=140,
#                                  explode=explode)

# ax.legend(wedges, categories, title="month", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
# plt.setp(autotexts, size=8, weight=700)
# ax.set_title("Biểu đồ thể hiện số lượng bài đăng theo tháng của năm 2020")
# plt.show()





#2, Bieu do the hien gia ban nha dat theo thoi gian tu thang 3 -12
month_price = month_df[month_df['price'].notnull()]
month_price_df = month_price.loc[(month_price['price'] != 'Thỏa thuận')]
month_price_df['price'] =  month_price_df['price'].apply(lambda x : float(x))

df2 = month_price_df.loc[(month_price_df['price'] < 10000)]
# 2.1 loai bo outliners cua price
sns.boxplot(x=df2['price'])
plt.show()
import pdb; pdb.set_trace()

df2 = month_price_df.groupby('month')['price'].sum().reset_index(name='total amount of money')
n = df2['month'].unique().__len__()+1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

# Plot Bars
plt.figure(figsize=(16,10), dpi= 80)
plt.bar(df2['month'], df2['total amount of money'], color=c, width=.5)
for i, val in enumerate(df2['total amount of money'].values):
    plt.text(i, val, float(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})

# Decoration
plt.gca().set_xticklabels(df2['month'], rotation=60, horizontalalignment= 'right')
plt.title("Bieu do the hien gia ban nha dat theo thoi gian tu thang 3 -12", fontsize=22)
plt.ylabel('total amount of money')
plt.show()


import pdb; pdb.set_trace()
#Quận
print(df['district'].unique())
#Phường
print(df['district'].unique())
#diện tích
print(df['square'].unique())

print("DONE")

