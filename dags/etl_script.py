import logging
import os
from dags.helper_functions import fetch_data, clean_data, transform_data, load_data_to_postgresql
import psycopg2

def main():
    logging.info("Starting data extraction process")
    url = "https://restcountries.com/v3.1/all"
    data = fetch_data(url)
    df_countries, df_country_languages = transform_data(data)
    df_countries, df_country_languages = clean_data(df_countries, df_country_languages)
    
    # Load database credentials from .env file
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    connection_string = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

    load_data_to_postgresql(df_countries, df_country_languages, connection_string)
    logging.info("Data loading process complete")

if __name__ == "__main__":
    main()