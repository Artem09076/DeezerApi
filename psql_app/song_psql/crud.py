"""This module include any action with db."""
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import models
from . import schemas


def get_song(db: Session, song_id: int):
    """Get song by id.

    Args:
        db (Session): session db
        song_id (int): song id

    Returns:
        Song model or none
    """
    return db.query(models.SongORM).where(models.SongORM.id == song_id).one_or_none()


def db_create_song(db: Session, song: schemas.SongAddModel):
    """Create new song with all relation.

    Args:
        db (Session): session db
        song (schemas.SongAddModel): song model

    Returns:
        id created song
    """
    db_song = models.SongORM(
        name=song.name,
        artist_name=song.artist_name,
        main_artist_name=song.main_artist_name,
        lyrics=song.lyrics,
        song_link=song.song_link,
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    db_album_music = models.AlbumMusicORM(
        artist_name=song.artist_name,
        main_artist=song.main_artist_name,
        album_name=song.album_name,
        song_name=song.name,
    )
    db.add(db_album_music)
    db.commit()
    db.refresh(db_album_music)
    return db_song.id


def get_result(db: Session, query: str):
    """Get resutl.

    Args:
        db (Session): session db
        query (str): query for search in db

    Returns:
        list with songs
    """
    search = text(
        """select
            s.id,
            s.name,
            s.main_artist_name,
            a.name,
            a.cover_link,
            a.date_realise
            from song s
        join album_music am on am.artist_name = s.artist_name and am.main_artist = s.main_artist_name and am.song_name = s."name"
        join album a on am.artist_name = s.artist_name and am.main_artist = s.main_artist_name and am.album_name = a."name"
        where s."name" ilike '%{search_query}%' ORDER BY a.date_realise desc""".format(
            search_query=query,
        ),
    )
    return db.execute(search).all()


def delete_song(db: Session, song_name: str):
    """Delete songs by his name.

    Args:
        db (Session): session db
        song_name (str): song name

    Returns:
        count song was delete
    """
    row_count = db.query(models.SongORM).filter_by(name=song_name).delete()
    db.commit()
    return row_count
