import pandas as pd
import pymysql
from sqlalchemy import create_engine
import argparse

if __name__ == "__main__":
    db_connection_str = 'mysql+pymysql://root:qwer1234@10.233.56.154/trainset'
    db_connection = create_engine(db_connection_str)
    try:
        conn = db_connection.connect()
        print('DB connect Success.')

        sql_statement = ''' SELECT * FROM traindf'''
        dataset = pd.read_sql(sql=sql_statement, con=conn)
        conn.close()
        print('Data Load Complete.')
    except:
        print('DB connect Fail.')
    dataset = dataset[dataset['number']==1]
    dataset.to_csv('/dataset.csv', index=False)
