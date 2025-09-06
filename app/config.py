import os

driver = os.getenv("DB_DRIVER", "postgresql")
host = os.getenv("DB_HOST", "localhost")
username = os.getenv("DB_USERNAME", "postgres")
password = os.getenv("DB_PASSWORD", "postgres")
port = os.getenv("DB_PORT", "5432")
database_name = os.getenv("DB_NAME", "db_fastapi")
