import collections
import pandas as pd
import surprise
import sqlite3 as sq
import sklearn

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
                FROM books
                WHERE LENGTH(STAR_RATING) < 2
                LIMIT 1000''', conn)

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


#from surprise import KNNBasic, SVD
#from surprise import NMF, model_selection

#KNN   - NOT WORKING --TOO MEMORY INTENSIVE
#algo = KNNBasic()
#model_selection.cross_validate(algo, data, measures=['RMSE'])


# svd
#algo = SVD()
#model_selection.cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)

# nmf
#algo = NMF()
#model_selection.cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)



from collections import defaultdict

from surprise import SVD



def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10
    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for userID, itemID, true_r, est, _ in predictions:
        top_n[userID].append((itemID, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for userID, rating in top_n.items():
        rating.sort(key=lambda x: x[1], reverse=True)
        top_n[userID] = rating[:n]

    return top_n


# First train an SVD algorithm on the dataset.
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
for userID, rating in top_n.items():
    print(userID, [itemID for (itemID, _) in rating])
