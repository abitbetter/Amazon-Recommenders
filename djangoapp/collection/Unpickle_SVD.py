import numpy as np
import _pickle as pickle
import pandas as pd
import sqlite3 as sql
#from sklearn.neighbors import NearestNeighbors

#may need to move into function
#wrangled_data = "/wrangled_knn_data.db"

def unpickle_corr():
    file = open("/db/svd_model_output2.p",'rb')
    corr = pickle.load(file)
    file.close()
    return corr

def unpickle_titles():
    file2 = open("/db/svd_book_titles.p",'rb')
    book_title = pickle.load(file2)
    file2.close()
    return book_title

def print_recs(book_title, corr, title):
    book_list = book_title.tolist()
    book_title = np.asarray(book_title)

    book_idx = book_list.index(title)
    corr_target = corr[book_idx]
    corrs = np.concatenate((book_title,corr_target),axis=0)

    top_5_idx = np.argsort(corr_target)[-6:-1]

    recs = ()
    for i in top_5_idx:
       recs = recs.append(book_title[i])
    return recs

#top_5_values = [book_title[i] for i in top_5_idx]



 #   print(top_5_values)


#print_recs(book_title, corr, "The Stand")


#corr = unpickle_corr()
#book_title = unpickle_titles()
#recs = print_recs(book_title, corr, "The Stranger Beside Me")
#print(recs)
