import numpy as np
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

dfBDS = pd.read_csv("newdfBDS.csv", dtype = {"id":"str", "month": "str"})
# dfBDS = pd.read_csv("newdfBDS.csv")

# dfBDS_copy = dfBDS.copy()
# train_set = dfBDS_copy.sample(frac=0.8, random_state=1)
# test_set = dfBDS_copy.drop(train_set.index)

train_set , test_set = train_test_split(dfBDS, test_size=0.2, random_state=42, shuffle=True)

# train_path = Path(data_dir, 'train_set.csv')
# test_path = Path(data_dir, 'test_set.csv')

train_set.to_csv(r'train_set.csv', index = False, header=True)
test_set.to_csv(r'test_set.csv', index = False, header=True)

print('DONE')