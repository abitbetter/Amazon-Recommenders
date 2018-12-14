import _pickle as pickle
import pandas as pd
import sqlite3 as sql
from sklearn.neighbors import NearestNeighbors

#may need to move into function
wrangled_data = "/db/wrangled_knn_data.db"

def unpickle():
    file = "/db/finalized_model.sav"
    clf = pickle.load(open(file, "rb"))
    return clf

def get_index_from_name(name, review_data):
    return review_data[review_data["product_title"]==name].index.tolist()[0]

def open_data(path):
    conn = sql.connect(path)
    #replace this with a query
    df = pd.read_sql("SELECT * FROM wrangled_books", conn)
    return(df)

def print_similar_books(review_data,query=None,id=None, model=None):

    distances2, indices2 = model.kneighbors(n_neighbors=5)
    if id:
        for id in indices2[id][1:]:
            print(review_data.iloc[id]["product_title"])
    if query:        
        found_id = get_index_from_name(query, review_data)
        counter=0
        recs={}
        for id in indices2[found_id][1:]:
            counter+=1
            recs[str(counter)]=review_data.iloc[id]["product_title"]
        return recs
           # print(indices2[found_id])


# model = unpickle()
# df = open_data(wrangled_data)
# recs = print_similar_books(df, query="The Stranger Beside Me", model=model)
# print(recs)
