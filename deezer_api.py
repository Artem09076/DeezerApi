"""This module contain function get discography artist."""

import requests
from fastapi.exceptions import HTTPException

from config import NOTFOUND


def extract_fields(info_data, fields_name):
    """Extract values from a dictionary by a list of keys.

    Args:
        info_data (dict): The dictionary containing the data.
        fields_name (list): The list of keys to extract values for.

    Returns:
        list: A list of values corresponding to the specified keys.
    """
    return [info_data.get(field_name) for field_name in fields_name]


def get_info_by_id(url: str, fields_name: tuple[list]):
    """Get info about artist ot album by id.

    Args:
        url (str): url for request.
        fields_name (tuple[list]): field names for which we collect data

    Returns:
        List with info about artist or album
    """
    respone = requests.get(url)
    data_info = respone.json()
    return extract_fields(data_info, fields_name)


def get_info_track(url: str, fields_artist_name: tuple[str], fields_album_name: tuple[str], fields_track_name: tuple[str]):
    """Get info about track.

    Args:
        url (str): url for request.
        fields_artist_name (tuple[str]): field names for which we collect data about artist
        fields_album_name (tuple[str]): field names for which we collect data about album
        fields_track_name (tuple[str]): field names for which we collect data about track

    Raises:
        HTTPException: if we can't find track

    Returns:
        Tuple of list with info about track his artist and album
    """
    respone = requests.get(url)
    data_info = respone.json()
    album_data = data_info.get('album')
    artist_data = data_info.get('artist')
    if not (album_data or artist_data):
        raise HTTPException(NOTFOUND, 'track not found')
    album_info = extract_fields(album_data, fields_album_name)
    artist_info = extract_fields(artist_data, fields_artist_name)
    track_info = extract_fields(data_info, fields_track_name)
    return album_info, artist_info, track_info


def get_serach_info(query: str, type_search: str, fields_name: tuple[str]):
    """Get search info.

    Args:
        query (str): query
        type_search (str): what we search(artist, album, track)
        fields_name (tuple[str]): field names for which we collect data

    Returns:
        List with info about artists, tracks, albums
    """
    search_url = f'https://api.deezer.com/search/{type_search}'
    search_result = {'q': query}
    respone = requests.get(search_url, search_result)
    data_info = respone.json()['data']
    list_info = []
    boards = 3 if len(data_info) > 3 else len(data_info)
    for index in range(boards):
        info_data = data_info[index]
        type_search_info = extract_fields(info_data, fields_name)
        list_info.append(type_search_info)
    return list_info


def get_search_result(query: str):
    """Get search result.

    Args:
        query (str): query

    Returns:
        Dict with ifnformation aboun artist, track, album
    """
    track_fields = ('id', 'title')
    albums_fields = ('id', 'title')
    artists_fields = ('id', 'name')
    search_result = {}
    search_result['artists'] = get_serach_info(query, 'artist', artists_fields)
    search_result['tracks'] = get_serach_info(query, 'track', track_fields)
    search_result['albums'] = get_serach_info(query, 'album', albums_fields)
    return search_result


def get_tracklist(url: str):
    """Get album or artist tracklist.

    Args:
        url (str): url for request

    Returns:
        List with data about  album or artist tracklist
    """
    tracklist_fields = ('id', 'title', 'preview')
    respone = requests.get(url)
    tracklist_data = respone.json().get('data', [])
    list_info = []
    for info_data in tracklist_data:
        type_search_info = extract_fields(info_data, tracklist_fields)
        list_info.append(type_search_info)
    return list_info
