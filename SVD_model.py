import pandas as pd
import sqlite3 as sq
import numpy as np
import _pickle as p

#Set up data
path = '/db/amazon_book_reviews_final.db'
def import_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT *
                FROM processed
                ;
                ''', conn)

    df['star_rating'] = df['star_rating'].astype(float)
    df['star_rating'] = df['star_rating'].astype(int) #convert rating to integer type
    df['helpful_votes'] = df['helpful_votes'].astype(int) #convert rating to integer type  


    return df

df = import_data(path)



from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
df_pivot = df.pivot_table(index='customer_id',columns='product_title',values='star_rating',fill_value=0)
X = df_pivot.T
SVD = TruncatedSVD(n_components=12, random_state=17)
matrix = SVD.fit_transform(X)
corr = np.corrcoef(matrix)
book_title = df_pivot.columns


def print_recs(book_title, corr, title):
    book_list = book_title.tolist()
    book_title = np.asarray(book_title)

    book_idx = book_list.index(title)
    corr_target = corr[book_idx]
    corrs = np.concatenate((book_title,corr_target),axis=0)

    top_5_idx = np.argsort(corr_target)[-6:-1]
    top_5_values = [book_title[i] for i in top_5_idx]
    print(top_5_values)


print_recs(book_title, corr, "The Stand")

#corr.dump("/db/svd_matrix_corrs")
outfile = "/db/svd_model_output2.p"
with open(outfile, 'wb') as pickle_file:
    p.dump(corr, pickle_file)



outfile2 = "/db/svd_book_titles.p"
with open(outfile2, 'wb') as pickle2:
    p.dump(book_title, pickle2)
