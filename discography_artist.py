"""This module contain function get discography artist."""
from datetime import date

import requests

from psql_app.config import OK


def get_artist_id(artist_name):
    """Get Artist id.

    Args:
        artist_name (_type_): artist name

    Returns:
        artist id or None
    """
    search_url = 'https://api.deezer.com/search/artist'
    search_result = {'q': artist_name}

    response = requests.get(search_url, params=search_result)
    if response.status_code == OK:
        result_data = response.json()
        if result_data['data']:
            return result_data['data'][0]['id']
        return None
    return None


def get_artist_albums(artist_id):
    """Get artist album.

    Args:
        artist_id: artist_id

    Returns:
        artist albums or None
    """
    if artist_id:
        albums_url = f'https://api.deezer.com/artist/{artist_id}/albums'
        response = requests.get(albums_url)
        if response.status_code == OK:
            result_data = response.json()
            return result_data['data']
        return None


def get_album_track(link_to_album: str):
    """Get album track.

    Args:
        link_to_album (str): link to album

    Returns:
        album track or None
    """
    response = requests.get(link_to_album)
    result_data = response.json()
    res = []
    for track in result_data['data']:
        res.append((track['title'], track['link'], count_artist(track['artist'])))
    return res


def get_discography(artist_name: str):
    """Get discography.

    Args:
        artist_name (str): artist name

    Returns:
        List of information about album artist
    """
    artist_id = get_artist_id(artist_name)
    artist_albums = get_artist_albums(artist_id)
    res = []
    for album in artist_albums:
        try:
            images_link = album['cover']
        except IndexError:
            images_link = None
        try:
            realise_date = date.fromisoformat(album['release_date'])
        except ValueError:
            realise_date = date(int(album['release_date']), 1, 1)
        album_type = album['record_type']
        res.append(
            (
                album['title'],
                album_type,
                realise_date,
                album['link'],
                images_link,
                album['tracklist'],
                [artist_name],
                get_total_track(album['tracklist']),
            ),
        )
    return sorted(res, key=lambda artist_name: artist_name[2], reverse=True)


def get_total_track(link_to_album: str):
    """Get total track album.

    Args:
        link_to_album (str): link to album

    Returns:
        total track
    """
    response = requests.get(link_to_album)
    search_data = response.json()
    return search_data['total']


def count_artist(res_data: dict) -> int:
    """Count artist.

    Args:
        res_data (dict): data result

    Returns:
        list of artist
    """
    artist_names = res_data['name']
    if isinstance(artist_names, str):
        return [artist_names]
    res = []
    for artist in artist_names:
        res.append(artist)
    return res
