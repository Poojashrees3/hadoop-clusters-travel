from hdfs import InsecureClient  # Assuming your custom package is similar
import pandas as pd
from sqlalchemy import create_engine
import os

# hdfs config
hdfs_url = 'http://100.114.53.18:9870'
client = InsecureClient(hdfs_url, user='hadoop', timeout=60)
 
# List of CSV files and corresponding mysql table names
hdfs_files = {
    '/home/hadoop/data/nameNode/Hotels.csv': 'hotels',
    '/home/hadoop/data/nameNode/Reviews.csv': 'reviews',
    '/home/hadoop/data/nameNode/Images.csv': 'hotel_images',
    '/home/hadoop/data/nameNode/Prices.csv': 'prices',
    '/home/hadoop/data/nameNode/Flights.csv': 'flights'
}
 
# mysql Database Configuration
db_user = 'root'
db_password = '123123'
db_host = '100.114.53.18'       
db_port = '3306'                 
db_name = 'march_vacation'             
 
# Connect to mysql
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
 
# Adding files from hdfs to mysql
for hdfs_file_path, table_name in hdfs_files.items():
    try:
        # Read CSV from HDFS into a pandas DataFrame
        with client.read(hdfs_file_path, encoding='utf-8') as reader:
            df = pd.read_csv(reader)
 
        print(f" Successfully read {hdfs_file_path} from HDFS.")
 
        
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        #
 
        print(f" Data successfully ingested into the '{table_name}' table in MySQL.\n")
 
    except Exception as e:
        print(f" Error during ingestion of {hdfs_file_path}: {e}\n")