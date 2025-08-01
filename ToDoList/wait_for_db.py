import time
import psycopg2
from psycopg2 import OperationalError
from decouple import config

print("Waiting for the database to be ready...")

while True:
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT')
        )
        connection.close()
        print("Database is ready!")
        break
    except OperationalError:
        print("Database not ready yet, retrying in 1 second...")
        time.sleep(1)