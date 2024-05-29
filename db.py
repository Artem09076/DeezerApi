from sqlalchemy import select
from sqlalchemy.orm import Session

from config import engine
from psql_app.models import ArtistORM, AlbumORM, SongORM, AlbumMusicORM


def insert_new_artist(artists: list[str]) -> None:
    with Session(engine) as session:
        artist_name = session.scalars(select(ArtistORM.name)).all()
        artists_for_add = []
        for artist in artists:
            if artist not in artist_name:
                artist_for_add = ArtistORM(name=artist)
                artists_for_add.append(artist_for_add)
        session.add_all(artists_for_add)
        session.commit()


def check_exists_song_in_db(
    song_name: str, song_artist_name: str, song_main_artist_name: str
):
    with Session(engine) as session:
        song = session.scalars(
            select(SongORM)
            .where(SongORM.name == song_name)
            .where(SongORM.artist_name == song_artist_name)
            .where(SongORM.main_artist_name == song_main_artist_name)
        ).one_or_none()
        return bool(song)


def check_relation(album_name: str, song_name: str, artist_name: str, main_artist: str):
    with Session(engine) as session:
        res = (
            session.query(AlbumMusicORM)
            .where(
                (AlbumMusicORM.album_name == album_name)
                & (AlbumMusicORM.artist_name == artist_name)
                & (AlbumMusicORM.song_name == song_name)
                & (AlbumMusicORM.main_artist == main_artist)
            )
            .one_or_none()
        )
        if res is not None:
            return False
        return True


def check_exists_album_in_db(
    album_name: str, album_main_artist_name: str, artist_name: str
) -> bool:
    with Session(engine) as session:
        album = (
            session.query(AlbumORM)
            .where(
                (AlbumORM.name == album_name)
                & (AlbumORM.main_artist_name == album_main_artist_name)
                & (AlbumORM.artist_name == artist_name)
            )
            .one_or_none()
        )
        if album is not None:
            return False
        return True
