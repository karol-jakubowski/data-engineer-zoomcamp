#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

def run():
    # 1. Zmienne konfiguracyjne
    year = 2021
    month = 1
    
    pguser = 'root'
    pgpassword = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'
    table_name = 'yellow_taxi_data'
    chunk_size = 100000

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    file_url = prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz'

    # 2. Definicja typów danych
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

    # 3. Połączenie z bazą
    print(f"Łączenie z bazą danych {pg_db}...")
    engine = create_engine(f'postgresql+psycopg://{pguser}:{pgpassword}@{pg_host}:{pg_port}/{pg_db}')

    # 4. Przygotowanie iteratora (czytanie pliku)
    print(f"Pobieranie i wczytywanie danych z: {file_url}")
    df_iter = pd.read_csv(
        file_url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )

    # 5. Inicjalizacja pierwszej paczki i założenie tabeli
    first_chunk = next(df_iter)
    
    first_chunk.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
    print("Struktura tabeli została utworzona.")

    first_chunk.to_sql(name=table_name, con=engine, if_exists="append")
    print(f"Wstawiono pierwszą paczkę: {len(first_chunk)} wierszy.")

    # 6. Pętla główna wstawiająca resztę pliku
    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(name=table_name, con=engine, if_exists="append")

    print("Zakończono wgrywanie danych pomyślnie!")

# Standardowy sposób uruchamiania głównej funkcji w Pythonie
if __name__ == '__main__':
    run()