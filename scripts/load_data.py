# data_storage.py
import os
import pandas as pd
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Set up logging
logging.basicConfig(
    filename='data_storage.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to create a connection engine
def get_engine():
    try:
        DB_NAME = os.getenv('DB_NAME')
        USER = os.getenv('DB_USER')
        PORT = os.getenv("DB_PORT")
        PASSWORD = os.getenv('DB_PASSWORD')
        HOST = os.getenv('DB_HOST', 'localhost')  # Default is localhost

        # Create the PostgreSQL connection engine
        engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
        logging.info('Database connection engine created successfully.')
        return engine
    except Exception as e:
        logging.error(f"Error creating database connection: {e}")
        raise

# Function to store data into the database
def store_data_in_db(dfs, engine, table_prefix='cleaned_data'):
    try:
        for i, df in enumerate(dfs):
            table_name = f"{table_prefix}_{i}"  # Create a unique table name for each dataframe
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logging.info(f"Stored dataframe {i} in table '{table_name}' successfully.")
    except Exception as e:
        logging.error(f"Error storing data to database: {e}")
        raise

# Function to load CSV files into dataframes
def load_csv_files(directory):
    dataframes = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(directory, filename))
                dataframes.append(df)
                logging.info(f"Loaded CSV file: {filename}.")
        return dataframes
    except Exception as e:
        logging.error(f"Error loading CSV files: {e}")
        raise
