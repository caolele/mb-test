# load precessed training dataset
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_pickle("./data/train.pkl")
df.tail()

dcec_feature_list = ['company_uuid', 'investor_names', 'investor_count', 
         'weeks_announced_quant', 'invest_phase', 'raised_amount_usd_quant', 
         'investor_count_imp', 'investor_count_log']
df = df[dcec_feature_list]
df[df.investor_names.notnull()].tail()

# Pad all timeseries to 28 elements, which is the query result from big query
cache = []
for index, row in df.iterrows():
    key = row['company_uuid']
    value = None
    if type(row['investor_count']) is not list:
        value = [0 for _ in range(868)]
    else:
        value = np.concatenate([row['investor_names'], 
                                row['invest_phase'],
                                row['weeks_announced_quant'], 
                                np.asarray(row['investor_count'])[:,np.newaxis], 
                                row['raised_amount_usd_quant'], 
                                np.asarray(row['investor_count_imp'])[:,np.newaxis], 
                                np.asarray(row['investor_count_log'])[:,np.newaxis]], axis=1).flatten()
        if len(value) > 868:
            value = value[:868]
        elif len(value) < 868:
            value = np.pad(value, (0, 868-len(value)), 'constant', constant_values=(0, 0))
        assert(len(value) == 868)
        
        if index % 1000 == 0 and index != 0:
            print(index)
        
    cache.append([key, value])

cdf = pd.DataFrame(cache, columns=['company_uuid', 'ts_feature'])
            
cdf.head(n=2)    

with open('dcec2.json', 'w') as f:
    f.write(cdf.to_json(orient='records')[1:-1].replace('},{', '}\n{'))