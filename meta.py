import pandas as pd
from pandas.io.json import json_normalize
import json
import gzip as gz
import sqlite3 as sq

def parse(path):
  g = gz.open(path, 'r')
  for l in g:
    yield eval(l)

def get_dict(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return df


def flatten_all(dictionary):
    out = {}
    out['product_id'] = dictionary['asin']
    if 'description' in dictionary.keys(): 
        out['description'] = dictionary['description']
    else:
        out['description'] = ''
    if 'price' in dictionary.keys():
        out['price'] = dictionary['price']
    else:
        out['price'] = ''
    if 'salesRank' in dictionary.keys():
        out['salesRank'] = dictionary['salesRank']['Books']
    else:
        out['salesRank'] = ''
    if 'categories' in dictionary.keys():
        out['categories'] = ",".join(dictionary['categories'][0])
    else:
        out['categories'] = ''
    if 'brand' in dictionary.keys():
        out['brand'] = dictionary['brand']
    else:
        out['brand'] = ''
    if 'related' in dictionary.keys():
        if 'also_viewed' in dictionary['related'].keys():
            out['also_viewed'] = ",".join(dictionary['related']['also_viewed'])
        else:
            out['also_viewed'] = ''
        if 'also_bought' in dictionary['related'].keys():
            out['also_bought'] = ",".join(dictionary['related']['also_bought'])
        else:
            out['also_bought'] = ''
        if 'bought_together' in dictionary['related'].keys():
            out['bought_together'] = ",".join(dictionary['related']['bought_together'])
        else:
            out['bought_together'] = ''
    else:
        out['also_viewed'] = ''
        out['also_bought'] = ''
        out['bought_together'] = ''
    return out



meta_dict = get_dict('/db/meta_Books.gz')


final_df = pd.DataFrame()
counter=0
for x in meta_dict.keys():
    try:
        temp_flat = flatten_all(meta_dict[x])
    except:
        continue
    temp_df = pd.DataFrame(temp_flat, index=[counter])
    if not temp_flat:
        pass
    else:
        final_df = final_df.append(temp_df)
    counter+=1
    print(counter)


path = '/db/wrangled_reviews.db'
conn = sq.connect(path)
df.to_sql('metadata', conn, if_exists='replace')

