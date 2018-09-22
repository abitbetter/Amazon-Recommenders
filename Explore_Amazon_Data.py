import pandas as pd
import sqlite3 as sq
import os
import gzip

#TO-DO: DON'T INSERT DUPLICATE ROWS

def create(amazon_file_path, db_file_path, table_name):
    conn = sq.connect(db_file_path)
    chunksize = 100000
    i=0
    j=1
    for df in pd.read_csv(amazon_file_path, delimiter='\t', compression='gzip', chunksize=chunksize, iterator=True, error_bad_lines=False):
        df.index += j
        i+=1
        print(i)
        df.to_sql(table_name, conn, if_exists='append')
        j = df.index[-1] + 1

def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)

def getDF(path, table_name, db_file_path):
    conn = sq.connect(db_file_path)
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    table = pd.DataFrame.from_dict(df, orient='index')
    table.to_sql(table_name, conn, if_exists='append')
