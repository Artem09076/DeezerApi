import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_url() -> str:
    DEFAULT_PORT = 5555

    dotenv.load_dotenv()

    port = os.environ.get("PG_PORT")
    port = int(port) if port and port.isdigit() else DEFAULT_PORT
    host = os.environ.get("PG_HOST")
    dbname = os.environ.get("PG_DBNAME")
    user = os.environ.get("PG_USER")
    password = os.environ.get("PG_PASSWORD")

    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


engine = create_engine(get_db_url())

SessionLocal = sessionmaker(bind=engine, autoflush=False)
