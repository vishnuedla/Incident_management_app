import psycopg2

def connection_database():
    conn = psycopg2.connect(host="database",    # use 127.0.0.1 on Windows
            port=5432,          # Postgres default port
            user="vishnu",
            password="bichu@#123",
            dbname="postgres" )
    return conn

