"""Test for api."""
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from psql_app.config import BADREQUEST, NOTFOUND, OK, engine
from main import app
from psql_app.models import AlbumORM, ArtistORM, SongORM


def get_id(orm_model):
    """Get id.

    Args:
        orm_model: Model

    Returns:
        id
    """
    with Session(engine) as session:
        id_ = session.query(orm_model).all()[0].id
    return id_


client = TestClient(app)


def test_read_artist_album():
    """Good test for albums artist."""
    artist_id = get_id(ArtistORM)
    response = client.get(f'/artist/{artist_id}')
    assert response.status_code == OK


def test_fail_read_artist_album():
    """Bad test for albums artist."""
    response = client.get('/artist/helps')
    assert response.status_code == NOTFOUND
    assert response.json() == {'detail': 'Artist not found'}
    artist_id = get_id(ArtistORM)
    response = client.get(f'/artist/{artist_id}', params={'page': 120})
    assert response.status_code == BADREQUEST
    assert response.json() == {'detail': 'This page not exist'}


def test_read_artists():
    """Good test for artists."""
    response = client.get('/artist/')
    assert response.status_code == OK


def test_bad_read_artists():
    """Bad test for artists."""
    response = client.get('/artist/', params={'page': 120})
    assert response.status_code == BADREQUEST
    assert response.json() == {'detail': 'This page not exist'}


def test_read_album_song():
    """Good test for song album."""
    album_id = get_id(AlbumORM)
    response = client.get(f'/albums/{album_id}')
    assert response.status_code == OK


def test_fail_album_song():
    """Bad test for song album."""
    response = client.get('/albums/hospadepomogi')
    assert response.status_code == NOTFOUND
    assert response.json() == {'detail': 'Album not found'}


def test_read_song():
    """Good test for song."""
    song_id = get_id(SongORM)
    response = client.get(f'/songs/{song_id}')
    assert response.status_code == OK


def test_fail_read_song():
    """Bad test for song."""
    response = client.get('/songs/kakayapesnyaihochynaotdh')
    assert response.status_code == NOTFOUND
    assert response.json() == {'detail': 'Song not found'}


def test_fail_read_result():
    """Bad test for results."""
    response = client.get(
        '/results/', params={'search_query': 'dagospadeotpustitemenya'},
    )
    assert response.status_code == BADREQUEST
    assert response.json() == {'detail': 'Nothing came up on your request'}
