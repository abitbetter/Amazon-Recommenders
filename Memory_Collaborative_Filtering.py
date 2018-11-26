# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:21:14 2018

@author: arjun
"""
#HAVING!!!!


import pandas as pd
import numpy as np
import sqlite3 as sq
from math import sqrt
from scipy import stats, spatial
from scipy.sparse import csr_matrix

#TO-DO: SHOULD I ONLY DO THIS WITH USERS WITH OVER A CERTAIN AMOUNT OF RATINGS?

def import_standard_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                      A.customer_id,
                      A.product_id,
                      A.product_title,
                      A.review_body,
                      A.STAR_RATING
                FROM
                    amazon_books_reviews A
                    JOIN
                    Product_Frequency_Rankings B ON B.product_id = A.product_id
                    JOIN
                    User_Frequency_Rankings C ON C.customer_id = A.customer_id
                WHERE LENGTH(STAR_RATING) < 2
                AND   B.COUNTS >= 58
                AND   C.COUNTS > 32
                ''', conn)

    df = df.reset_index(drop=True)
    return df

def retrieve_user_counts(db_path):
        conn = sq.connect(db_path) #sqliteDB path goes in parantheses
        crsr = conn.cursor()

        df = pd.read_sql_query('''
                    SELECT DISTINCT
                          A.customer_id,
                          COUNT(A.STAR_RATING)
                    FROM
                        amazon_books_reviews A
                    GROUP BY
                        A.customer_id
                    ''', conn)
        return df

def retrieve_product_counts(db_path):
        conn = sq.connect(db_path) #sqliteDB path goes in parantheses
        crsr = conn.cursor()

        df = pd.read_sql_query('''
                    SELECT DISTINCT
                          A.product_id,
                          COUNT(A.STAR_RATING)
                    FROM
                        amazon_books_reviews A
                    GROUP BY A.product_id
                    ''', conn)
        return df


def import_product_frequency_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                      Z.product_id,
                      Z.counts
                FROM
                    Product_Frequency_Rankings Z
                ''', conn)

    df = df.reset_index(drop=True)
    return df

def import_user_frequency_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                      Z.customer_id,
                      Z.counts
                FROM
                    User_Frequency_Rankings Z
                ''', conn)

    df = df.reset_index(drop=True)
    return df

def euclidean_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = {}

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated[item]=1
    if len(both_rated)<1:  #work this into distance formula to account for volume
        return 0

    euclidean_distance = []

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            u1_avg_rating = np.mean(u1_data['star_rating'].loc[u1_data['product_id']==item].tolist())
            u2_avg_rating = np.mean(u2_data['star_rating'].loc[u2_data['product_id']==item].tolist())

            euclidean_distance.append((u1_avg_rating - u2_avg_rating)**2)

    sum_of_euclidean_distance = sum(euclidean_distance)
    inverted_euclidean_distance = 1/(1+sqrt(sum_of_euclidean_distance))
    return inverted_euclidean_distance

def pearson_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = []

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated.append(item)

    if len(both_rated)<1:
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

    if len(both_rated)<1:
        return 0

    u1_data = u1_data['star_rating'][u1_data['product_id'].isin(both_rated)].tolist()
    u2_data = u2_data['star_rating'][u2_data['product_id'].isin(both_rated)].tolist()

    cosine_similarity = 1 - spatial.distance.cosine(u1_data, u2_data)
    return cosine_similarity


def user_user_collab(user, data, dictionary):
    dictionary['customers'].append(user)
    dictionary['top_1'].append('')
    dictionary['top_1_euclidean'].append(0)

    user_set = data['customer_id'].tolist()
    for x in user_set:
        check_set = set(dictionary['customers'])
        print(check_set)
        if x==user or x in check_set:
            continue
        elif x != user:
            print(x)
            euclidean_distance = euclidean_similarity(user, x, data)
        if euclidean_distance >= dictionary['top_1_euclidean'][-1]:
            dictionary['top_1'][-1]=x
            dictionary['top_1_euclidean'][-1]=euclidean_distance
        else:
            continue
    return dictionary


def main(df):
    dict = {'customers':[], 'top_1':[], 'top_1_euclidean':[]}
    for x in df['customer_id']:
        a = user_user_collab(x, df, dict)

    dataframe = pd.DataFrame.from_dict(a, orient='columns')
    return dataframe
