import numpy as np
import _pickle as pickle
import pandas as pd
import sqlite3 as sql


def unpickle_matrix():
    file = open("/db/lightfm_item_matrix2.p",'rb')
    item_item_matrix = pickle.load(file)
    file.close()
    return item_item_matrix

def unpickle_dict():
    file2 = open("/db/lightfm_movie_dict.p",'rb')
    movies_dict = pickle.load(file2)
    file2.close()
    return movies_dict


def item_item_recommendation(item_emdedding_distance_matrix, item_id, 
                             item_dict, n_items = 5, show = True):
    recommended_items = list(pd.Series(item_emdedding_distance_matrix.loc[item_id]. \
                                  sort_values(ascending = False).head(n_items+1). \
                                  index[1:n_items+1]))
    return recommended_items

item_item_dist = unpickle_matrix()
movies_dict = unpickle_dict()

rec_list = item_item_recommendation(item_emdedding_distance_matrix = item_item_dist,
                                    item_id = "The Stranger Beside Me",
                                    item_dict = movies_dict,
                                    n_items = 5, show=False)

print(rec_list)

