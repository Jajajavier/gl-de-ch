from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = "mariadb_user"
DB_PASS = "mariadb_password"
DB_HOST = "127.0.0.1"  # db docker compose service
DB_PORT = "3307"
DB_NAME = "globant_migration"
DB_CHARSET = "utf8mb4"  # utf8mb4
database_url = f"mariadb+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

# The echo=True parameter indicates that SQL emitted by connections will be logged to STDOUT
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
