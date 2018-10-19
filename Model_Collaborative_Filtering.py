import pandas as pd
import surprise

#Set up data
path = '/db/amazon_reviews.db'
def import_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                    customer_id,
                    product_id,
                    star_rating
                FROM amazon_music_reviews
                WHERE LENGTH(STAR_RATING) < 2
                AND product_id = 'B00Q9KEZV0' LIMIT 10000''', conn)

    df['star_rating'] = df['star_rating'].astype(float)
    df['star_rating'] = df['star_rating'].astype(int) #convert rating to integer type

    return df

df = import_data(path)


from surprise import Reader, Dataset

# to load dataset from pandas df, we need `load_fromm_df` method in surprise lib

ratings_dict = {'itemID': list(df.product_id),
                'userID': list(df.customer_id),
                'rating': list(df.star_rating)}
df = pd.DataFrame(ratings_dict)

# A reader is still needed but only the rating_scale param is required.
# The Reader class is used to parse a file containing ratings.
reader = Reader(rating_scale=(1, 5))

# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)




# Split data into 5 folds

data.split(n_folds=5)

from surprise import SVD, evaluate
from surprise import NMF

# svd
algo = SVD()
evaluate(algo, data, measures=['RMSE'])

# nmf
algo = NMF()
evaluate(algo, data, measures=['RMSE'])
