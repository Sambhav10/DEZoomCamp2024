
from time import time
import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port= params.port
    db= params.db
    table_name = params.table_name
    url = params.url

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df_iter = pd.read_csv(url, iterator=True, chunksize=100000)
    df = next(df_iter)
    
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    df.head(n = 0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    # Injest data

    while True: 
        start_time = time()
        df=next(df_iter)
        
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        df.to_sql(name=table_name, con=engine, if_exists='append')

        end_time = time()
        print('inserted another chunk... took %.3f seconds' %(end_time - start_time))
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Injest CSV data to Postgres.')

    #user, password, host , port , database name, table name, url of the csv

    parser.add_argument('--user',   help='username for postgres')
    parser.add_argument('--password',   help='password for postgres')
    parser.add_argument('--host',   help='host for postgres')
    parser.add_argument('--port',   help='port for postgres')
    parser.add_argument('--db',   help='database name for postgres')
    parser.add_argument('--table_name',   help='name of the table where we will write to')
    parser.add_argument('--url',   help='url of the csv file ')

    args = parser.parse_args()
    
main(args)




