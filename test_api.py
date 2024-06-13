"""This module include test on pages."""
from fastapi.testclient import TestClient

from config import BADREQUEST, NOTFOUND, OK
from main import app

client = TestClient(app)


def test_read_root():
    """Test root page."""
    response = client.get('/')
    assert response.status_code == OK


def test_read_results_success():
    """Success test results page."""
    search_query = 'test'
    response = client.get(f'/results/?search_query={search_query}')
    assert response.status_code == OK


def test_read_results_fail():
    """Fail test results page."""
    search_query = 'test_query'
    response = client.get(f'/results/?search_query={search_query}')
    assert response.status_code == BADREQUEST


def test_read_artist_success():
    """Success test artist page."""
    artist_id = 27
    response = client.get(f'/artist/{artist_id}')
    assert response.status_code == OK


def test_read_page_artist_fail():
    """Fail test artist page."""
    artist_id = 123456765432
    response = client.get(f'/artist/{artist_id}')
    assert response.status_code == NOTFOUND


def test_read_album_success():
    """Success test album page."""
    album_id = 302127
    response = client.get(f'/album/{album_id}')
    assert response.status_code == OK


def test_read_album_fail():
    """Fail test album page."""
    album_id = 12345678765432
    response = client.get(f'/album/{album_id}')
    assert response.status_code == NOTFOUND


def test_read_track_success():
    """Success test track page."""
    track_id = 3135556
    response = client.get(f'/track/{track_id}')
    assert response.status_code == OK


def test_read_track_fail():
    """Fail test track page."""
    track_id = 1234567865432
    response = client.get(f'/track/{track_id}')
    assert response.status_code == NOTFOUND
