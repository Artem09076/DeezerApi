"""This module contain function for use db."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from psql_app.config import engine
from psql_app.models import AlbumMusicORM, AlbumORM, ArtistORM


def insert_new_artist(artists: list[str]) -> None:
    """Insert new artist.

    Args:
        artists (list[str]): list of artist
    """
    with Session(engine) as session:
        artist_name = session.scalars(select(ArtistORM.name)).all()
        artists_for_add = []
        for artist in artists:
            if artist not in artist_name:
                artist_for_add = ArtistORM(name=artist)
                artists_for_add.append(artist_for_add)
        session.add_all(artists_for_add)
        session.commit()


def check_relation(album_name: str, song_name: str, artist_name: str, main_artist: str):
    """Check existing relation.

    Args:
        album_name (str): album name
        song_name (str): song_name
        artist_name (str): artist name
        main_artist (str): main artist

    Returns:
        bool exist oor not
    """
    with Session(engine) as session:
        res = (
            session.query(AlbumMusicORM)
            .where(
                (AlbumMusicORM.album_name == album_name)
                & (AlbumMusicORM.artist_name == artist_name)
                & (AlbumMusicORM.song_name == song_name)
                & (AlbumMusicORM.main_artist == main_artist),
            )
            .one_or_none()
        )
        return not bool(res)


def check_exists_album_in_db(
    album_name: str, main_artist_name: str, artist_name: str,
) -> bool:
    """Check exist album in db.

    Args:
        album_name (str): album name
        main_artist_name (str): album main artist
        artist_name (str): artist name

    Returns:
        bool: exist or none
    """
    with Session(engine) as session:
        album = (
            session.query(AlbumORM)
            .where(
                (AlbumORM.name == album_name)
                & (AlbumORM.main_artist_name == main_artist_name)
                & (AlbumORM.artist_name == artist_name),
            )
            .one_or_none()
        )
        return not bool(album)
