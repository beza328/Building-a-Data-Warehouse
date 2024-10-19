import pandas as pd
import os
import logging
from PIL import Image
from sqlalchemy import create_engine


# Set up logging
logging.basicConfig(
    filename='data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define a function to load CSV files
def load_csv_files(directory):
    dataframes = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(directory, filename))
                dataframes.append(df)
                logging.info(f"Loaded file: {filename} with {len(df)} rows.")
            except Exception as e:
                logging.error(f"Error loading {filename}: {e}")
    return dataframes

# Step 1: Remove Duplicates
def remove_duplicates(dfs):
    for i in range(len(dfs)):
        original_length = len(dfs[i])
        dfs[i] = dfs[i].drop_duplicates()
        logging.info(f"Removed duplicates from dataset {i}. Original length: {original_length}, New length: {len(dfs[i])}.")
    return dfs

# Step 2: Handle Missing Values
def handle_missing_values(dfs):
    for i in range(len(dfs)):
        try:
            # Fill missing values with the mean for numerical columns
            dfs[i] = dfs[i].fillna(dfs[i].mean(numeric_only=True))  # Only for numeric columns
            logging.info(f"Handled missing values in dataset {i}.")
        except Exception as e:
            logging.error(f"Error handling missing values in dataset {i}: {e}")
    return dfs

# Step 3: Standardize Formats
def standardize_formats(dfs):
    for i, df in enumerate(dfs):
        for col in df.select_dtypes(include=['object']):
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                logging.info(f"Standardized format for column {col} in dataset {i}.")
            except Exception as e:
                logging.error(f"Could not convert column {col} in dataset {i}: {e}")
    return dfs

# Step 4: Data Validation
def validate_data(dfs):
    for i, df in enumerate(dfs):
        if 'amount' in df.columns:
            if (df['amount'] < 0).any():
                logging.warning(f"Negative values found in 'amount' column of dataset {i}.")

# Step 5: Store Cleaned Data
def store_cleaned_data(dfs, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for i, df in enumerate(dfs):
        try:
            df.to_csv(os.path.join(output_directory, f'cleaned_data_{i}.csv'), index=False)
            logging.info(f"Stored cleaned data for dataset {i} to {output_directory}.")
        except Exception as e:
            logging.error(f"Error storing cleaned data for dataset {i}: {e}")

# Step 6: Process Images
def process_images(image_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(image_directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_directory, filename)
            try:
                with Image.open(image_path) as img:
                    img = img.convert('RGB')  # Convert to RGB if necessary
                    img.save(os.path.join(output_directory, filename))  # Save processed image
                logging.info(f"Processed image: {filename}.")
            except Exception as e:
                logging.error(f"Error processing image {filename}: {e}")

