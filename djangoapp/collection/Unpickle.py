import _pickle as pickle
import pandas as pd
import sqlite3 as sql

#may need to move into function
wrangled_data = "C:/Users/mches/Dropbox/Georgetown Data Science -- Team Amazon/wrangled_knn_data.db"

def unpickle():
    file = r"C:\Users\mches\Documents\App\finalized_model.sav"
    clf = pickle.load(open(file, "rb"))
    return clf

def get_index_from_name(name, review_data):
    return review_data[review_data["product_title"]==name].index.tolist()[0]

def print_similar_books(review_data,query=None,id=None, model=None):
    conn = sql.connect(review_data)
    #replace this with a query
    df = pd.read_sql(review_data,conn)
    return print(len(df))

print_similar_books(wrangled_data)


    #
    # distances2, indices2 = model.kneighbors()
    # if id:
    #     for id in indices2[id][1:]:
    #         print(review_data.iloc[id]["product_title"])
    # if query:
    #     found_id = get_index_from_name(query, review_data)
    #     for id in indices2[found_id][1:]:
    #         print(review_data.iloc[id]["product_title"])
