from fastapi.testclient import TestClient
from main import app
from config import engine
from sqlalchemy.orm import Session
from psql_app.models import ArtistORM, AlbumORM, SongORM


def get_id(orm_model):
    with Session(engine) as session:
        id_ = session.query(orm_model).all()[0].id
    return id_


client = TestClient(app)


def test_read_artist_album():
    artist_id = get_id(ArtistORM)
    response = client.get(f"/artist/{artist_id}")
    assert response.status_code == 200


def test_fail_read_artist_album():
    response = client.get("/artist/helps")
    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}
    artist_id = get_id(ArtistORM)
    response = client.get(f"/artist/{artist_id}", params={"page": 120})
    assert response.status_code == 400
    assert response.json() == {"detail": "This page not exist"}


def test_read_artists():
    response = client.get("/artist/")
    assert response.status_code == 200


def test_bad_read_artists():
    response = client.get("/artist/", params={"page": 120})
    assert response.status_code == 400
    assert response.json() == {"detail": "This page not exist"}


def test_read_album_song():
    album_id = get_id(AlbumORM)
    response = client.get(f"/albums/{album_id}")
    assert response.status_code == 200


def test_fail_album_song():
    response = client.get("/albums/hospadepomogi")
    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}


def test_read_song():
    song_id = get_id(SongORM)
    response = client.get(f"/songs/{song_id}")
    assert response.status_code == 200


def test_fail_read_song():
    response = client.get("/songs/kakayapesnyaihochynaotdh")
    assert response.status_code == 404
    assert response.json() == {"detail": "Song not found"}


def test_read_result():
    response = client.get("/results/", params={"search_query": "a"})
    assert response.status_code == 200


def test_fail_read_result():
    response = client.get(
        "/results/", params={"search_query": "dagospadeotpustitemenya"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Nothing came up on your request"}


def test_read_artist():
    response = client.get("/artists/")
    assert response.status_code == 200
