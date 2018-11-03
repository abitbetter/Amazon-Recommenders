# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:21:14 2018

@author: arjun
"""

import pandas as pd
import numpy as np
import sqlite3 as sq
from math import sqrt
from scipy import stats, spatial
from scipy.sparse import csr_matrix

path = 'C:/users/arjun/Desktop/amazon.db'

#TO-DO: SHOULD I ONLY DO THIS WITH USERS WITH OVER A CERTAIN AMOUNT OF RATINGS?

def import_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                    X.customer_id,
                    X.product_id,
                    X.star_rating,
                    X.PRODUCTS_REVIEWED
                FROM
                    (SELECT
                        customer_id,
                        product_id,
                        star_rating,
                        COUNT(product_id) AS products_reviewed
                    FROM
                        amazon_music_reviews
                    GROUP BY
                        customer_id,
                        product_id,
                        star_rating) X
                WHERE LENGTH(STAR_RATING) < 2
                AND   X.PRODUCTS_REVIEWED > 20
                ''', conn)

    df['star_rating'] = df['star_rating'].astype(float)
    df['star_rating'] = df['star_rating'].astype(int) #convert rating to integer type
    df = df.reset_index()
    return df

df = import_data(path)

def euclidean_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = {}

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated[item]=1

    if len(both_rated)<=1:  #work this into distance formula to account for volume
        return 0

    euclidean_distance = []

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            u1_avg_rating = np.mean(u1_data['star_rating'].loc[u1_data['product_id']==item].tolist())
            u2_avg_rating = np.mean(u2_data['star_rating'].loc[u2_data['product_id']==item].tolist())

            euclidean_distance.append((u1_avg_rating - u2_avg_rating)**2)

    sum_of_euclidean_distance = sum(euclidean_distance)
    inverted_euclidean_distance = 1/(1+sqrt(sum_of_euclidean_distance))
    return user1, user2, inverted_euclidean_distance



def pearson_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = []

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated.append(item)

    if len(both_rated)<=1:
        return 0

    u1_data = u1_data['star_rating'][u1_data['product_id'].isin(both_rated)].tolist()
    u2_data = u2_data['star_rating'][u2_data['product_id'].isin(both_rated)].tolist()

    pearson_corr = stats.pearsonr(u1_data, u2_data)
    return pearson_corr[0]


def cosine_similarity(user1, user2, data):
    both_rated = []

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated.append(item)

    if len(both_rated)<=1:
        return 0

    u1_data = u1_data['star_rating'][u1_data['product_id'].isin(both_rated)].tolist()
    u2_data = u2_data['star_rating'][u2_data['product_id'].isin(both_rated)].tolist()

    cosine_similarity = 1 - spatial.distance.cosine(u1_data, u2_data)
    return cosine_similarity


def final_function(user, data, dictionary):
    dictionary['customers'].append(user)
    dictionary['top_1'].append('')
    dictionary['top_1_pearson'].append(-1)

    user_set = data['customer_id'].tolist()
    for x in user_set:
        pearson_corr = cosine_similarity(user, x, data)
        print(dictionary['top_1_pearson'][-1])
        if pearson_corr >= dictionary['top_1_pearson'][-1]:
            dictionary['top_1'][-1]=x
            dictionary['top_1_pearson'][-1]=pearson_corr
        else:
            pass
    return dictionary


def main():
    dict = {'customers':[], 'top_1':[], 'top_1_pearson':[]}
    for x in df['customer_id']:
        a = final_function(x, df, dict)

    dataframe = pd.DataFrame.from_dict(a, orient='columns')
    return dataframe



dataframe = main()
print(dataframe.head(25))
