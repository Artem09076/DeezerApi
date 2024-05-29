from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import models
from . import schemas


def get_song(db: Session, song_id: int):
    return db.query(models.SongORM).where(models.SongORM.id == song_id).one_or_none()


def db_create_song(db: Session, song: schemas.SongAddModel):
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
            search_query=query
        )
    )
    res = db.execute(search).all()
    return res


def delete_song(db: Session, song_name: str):
    row_count = db.query(models.SongORM).filter_by(name=song_name).delete()
    db.commit()
    return row_count
