import pandas as pd
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(url):
    logging.info(f"Fetching data from {url}")
    response = requests.get(url)
    logging.info(f"Data fetched successfully from {url}")
    return response.json()

def extract_country_data(country, idx):
    country_id = idx
    country_name = country.get('name', {}).get('common', '')
    independence = country.get('independent', False)
    un_member = country.get('unMember', False)
    start_of_week = country.get('startOfWeek', '')
    official_name = country.get('name', {}).get('official', '')
    native_names = country.get('name', {}).get('nativeName', {})
    common_native_name = ', '.join([native_name.get('common', '') for native_name in native_names.values()])
    
    currency_info = country.get('currencies', {})
    if currency_info:
        currency_code = list(currency_info.keys())[0]
        currency_name = currency_info[currency_code].get('name', '')
        currency_symbol = currency_info[currency_code].get('symbol', '')
    else:
        currency_code = currency_name = currency_symbol = ''

    idd = country.get('idd', {})
    idd_root = idd.get('root', '')
    idd_suffixes = idd.get('suffixes', [])
    country_code = ', '.join([idd_root + suffix for suffix in idd_suffixes])
    
    capital = ', '.join(country.get('capital', []))
    region = country.get('region', '')
    subregion = country.get('subregion', '')
    area = country.get('area', 0)
    population = country.get('population', 0)
    continents = ', '.join(country.get('continents', []))
    
    languages = country.get('languages', {})
    
    country_data = {
        'country_id': country_id,
        'country_name': country_name,
        'independence': independence,
        'united_nations_member': un_member,
        'start_of_week': start_of_week,
        'official_name': official_name,
        'common_native_name': common_native_name,
        'currency_code': currency_code,
        'currency_name': currency_name,
        'currency_symbol': currency_symbol,
        'country_code': country_code,
        'capital': capital,
        'region': region,
        'subregion': subregion,
        'area': area,
        'population': population,
        'continents': continents
    }
    
    language_data = [{'country_id': country_id, 'country_name': country_name, 'language_code': lang_code, 'language_name': lang_name} for lang_code, lang_name in languages.items()]

    return country_data, language_data

def transform_data(data):
    logging.info("Transforming data")
    countries_data = []
    languages_data = []
    
    for idx, country in enumerate(data, start=1):
        country_data, language_data = extract_country_data(country, idx)
        countries_data.append(country_data)
        languages_data.extend(language_data)
    
    df_countries = pd.DataFrame(countries_data)
    df_country_languages = pd.DataFrame(languages_data)
    logging.info("Data transformation complete")
    
    return df_countries, df_country_languages

def clean_data(df_countries, df_country_languages):
    logging.info("Cleaning data")
    df_countries.loc[df_countries['country_name'] == 'Russia', 'continents'] = 'Europe' 
    df_countries.loc[df_countries['country_name'] == 'Azerbaijan', 'continents'] = 'Asia'
    df_countries.loc[df_countries['country_name'] == 'Turkey', 'continents'] = 'Asia'
    df_countries.loc[df_countries['country_name'] == 'Christmas Island', 'continents'] = 'Oceania'
    df_countries.loc[df_countries['country_name'] == 'Cocos (Keeling) Islands', 'continents'] = 'Oceania'
    df_countries.loc[df_countries['country_name'] == 'British Indian Ocean Territory', 'continents'] = 'Africa'
    df_countries.loc[df_countries['country_name'] == 'United States Minor Outlying Islands', 'continents'] = 'North America'
    df_countries.loc[df_countries['country_name'] == 'Timor-Leste', 'continents'] = 'Asia'

    df_countries = df_countries[df_countries['country_name'] != 'Antarctica']

    df_country_languages = df_country_languages[['country_id', 'language_code', 'language_name']]

    logging.info("Data cleaning complete")
    return df_countries, df_country_languages

def load_data_to_postgresql(df_countries, df_country_languages, connection_string):
    logging.info("Loading data to PostgreSQL database")
    try:
        engine = create_engine(connection_string)
        df_countries.to_sql('countries', engine, if_exists='replace', index=False)
        df_country_languages.to_sql('country_languages', engine, if_exists='replace', index=False)
        logging.info("DataFrames have been successfully loaded into the PostgreSQL database.")
    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")

