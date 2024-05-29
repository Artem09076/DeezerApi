from datetime import date

import requests


def get_artist_id(artist_name):
    search_url = "https://api.deezer.com/search/artist"
    params = {"q": artist_name}

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            artist_id = data["data"][0]["id"]
            return artist_id
        return None
    return None


def get_artist_albums(artist_id):
    if artist_id:
        albums_url = f"https://api.deezer.com/artist/{artist_id}/albums"
        response = requests.get(albums_url)
        if response.status_code == 200:
            data = response.json()
            albums = data["data"]
            return albums
        return None


def get_album_track(link_to_album: str):
    response = requests.get(link_to_album)
    data = response.json()
    res = []
    for track in data["data"]:
        res.append((track["title"], track["link"], count_artist(track["artist"])))
    return res


def get_discography(artist_name: str):
    artist_id = get_artist_id(artist_name)
    artist_albums = get_artist_albums(artist_id)
    res = []
    for data in artist_albums:
        try:
            images_link = data["cover"]
        except IndexError:
            images_link = None
        try:
            realise_date = date.fromisoformat(data["release_date"])
        except ValueError:
            realise_date = date(int(data["release_date"]), 1, 1)
        album_type = data["record_type"]
        res.append(
            (
                data["title"],
                album_type,
                realise_date,
                data["link"],
                images_link,
                data["tracklist"],
                [artist_name],
                get_total_track(data["tracklist"]),
            )
        )
    return sorted(res, key=lambda x: x[2], reverse=True)


def get_total_track(link_to_album: str):
    response = requests.get(link_to_album)
    data = response.json()
    return data["total"]


def count_artist(data: dict) -> int:
    artist_names = data["name"]
    if isinstance(artist_names, str):
        return [artist_names]
    res = []
    for artist in artist_names:
        res.append(artist)
    return res
