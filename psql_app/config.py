"""This module contain config data."""
import os

import dotenv
from sqlalchemy import create_engine

GENIUSTOKEN = 'zXxzPPAMIGKzUIh7Ojy1mTfNXEAohPfFoxwalDEAmwuCZvrWNdXWphwrJzSGapZB'

NOTFOUND = 404
BADREQUEST = 400
OK = 200
SONGRIGHTBROAD = 6000


def get_db_url() -> str:
    """Get db url.

    Returns:
        db url
    """
    default_port = 5555

    dotenv.load_dotenv()

    port = os.environ.get('PG_PORT')
    port = int(port) if port and port.isdigit() else default_port
    host = os.environ.get('PG_HOST')
    dbname = os.environ.get('PG_DBNAME')
    user = os.environ.get('PG_USER')
    password = os.environ.get('PG_PASSWORD')

    return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


engine = create_engine(get_db_url())


tags_metadata = [
    {
        'name': 'Artists',
        'description': 'Operations with artist.',
    },
    {
        'name': 'Albums',
        'description': 'Operations with album',
    },
    {
        'name': 'Songs',
        'description': 'Operations with spng',
    },
    {
        'name': 'Templates',
        'description': 'Here contain get request for page site',
    },
]
