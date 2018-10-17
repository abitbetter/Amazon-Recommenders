
# This is the data ingestion & exploration notebook. Please take note that the Explore_Amazon_Data module will read in and modify existing tables if you give it an existing table name.


import pandas as pd
import os 
import gzip
import sqlite3 as sq
import Explore_Amazon_Data as amzn  #This is our data ingestion module, please ensure that this python file is in the same folder as the Notebook.


# 1.) Defines the three inputs into the Explore_Amazon_Data module. amazon_file_path is the location of the raw aws customer review data. db_file_path is the location of the SQLite DB. table_name defines which table the data will be dumped into.
# 
# 2.) Run the ingestion module to read in raw files and dump to the specified tables in the SQLite database.



amazon_file_path = /db
db_file_path = /db/sql
table_name = 'trial'


amzn.create(amazon_file_path, db_file_path, table_name)


