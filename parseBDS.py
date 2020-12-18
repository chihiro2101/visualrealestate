import numpy as np
import pandas as pd
import json



def func(row):
    if len(str(row['price'])) == 3 or row['price'] == 'Thỏa thuận':
        return row['price']
    elif row['price'].find('tỷ') != -1 :
        return float(row['price'].split(' ')[0])*1000
    else:
        return float(row['price'].split(' ')[0])*row['area']

def findWard(x):
    if len(str(x)) == 3:
        return x
    elif x.lower().find('phường') != -1: 
        if x.find('-') != -1:
            x = x.replace('-', ',')
        return x.lower().split('phường')[1].split(',')[0].strip()
    else:
        return 'KXD'

def findDistrict(x):
    if len(str(x)) == 3:
        return x
    elif x.find(',') != -1:
        if x.lower().find('quận') != -1:
            return x.lower().split('quận')[1].split(',')[0].strip()
        else:
            return x.lower().split(',')[-2].strip()
    elif x.find('-') != -1:
        x = x.lower()
        if x.find('quận') != -1:
            return x.split('quận')[1].split('-')[0].strip()
        else:        
            return x.split('-')[-2].strip()
    else:
        return 'KXD'


def preprocess(data):
    #parse
    price = data.apply(func, axis = 1)
    square = data['area']
    bedrooms = data['bedrooms']
    bathrooms = data['toilets']
    # ward = data['address'].apply(lambda x: x if len(str(x)) == 3 else (x.split('Phường')[1].split(',')[0].strip() if x.lower().find('phường') != -1 else 'KXĐ'))
    ward = data['address'].apply(lambda x: findWard(x))
    # district = data['address'].apply(lambda x: x.split(',')[-2].strip() if len(str(x)) > 3 else x)
    district = data['address'].apply(lambda x : findDistrict(x))
    direction = data['direction']
    balcony_direction = data['balcony_direction']
    doc = data['law_doc'].apply(lambda x: 'đỏ' if str(x).lower().find('đỏ') != -1 else x).apply(lambda x: 'hồng' if str(x).lower().find('hồng') != -1 else x)
    law_doc = doc.apply(lambda x: 'có giấy tờ' if len(str(x)) > 4 else x)

    project = data['project']
    investor = data['investor']
    post_month = data['post_date'].apply(lambda x: x.split('/')[1].strip() if len(str(x)) > 3 else x)
    post_id = data['id']


    nhadatdf = {'id': post_id, 'month': post_month, 'project': project, 'investor': investor, 'square': square, 'bedrooms': bedrooms, 'bathrooms': bathrooms,'direction': direction,'balcony' : balcony_direction, 'district': district, 'ward': ward , 'law_doc': law_doc, 'price': price}
    dfBDS = pd.DataFrame(nhadatdf)
    return dfBDS


data1 = pd.read_json('data1_4000.json', orient='records')
data2 = pd.read_json('data4000_7500.json', orient='records')

df1 = preprocess(data1) 
df2 = preprocess(data2)
dfBDS = df1.append(df2, ignore_index = True) 

#dfBDS.to_csv (r'dfBDS.csv', index = False, header=True)

print('DONE')
