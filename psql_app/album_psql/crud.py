from sqlalchemy.orm import Session

from .. import models
from . import schemas


def get_album_songs(db: Session, album_id: str):
    res = (
        db.query(models.SongORM)
        .join(
            models.AlbumMusicORM,
            (models.SongORM.name == models.AlbumMusicORM.song_name)
            & (models.SongORM.artist_name == models.AlbumMusicORM.artist_name)
            & (models.SongORM.main_artist_name == models.AlbumMusicORM.main_artist),
        )
        .join(
            models.AlbumORM,
            (models.AlbumORM.name == models.AlbumMusicORM.album_name)
            & (models.AlbumMusicORM.artist_name == models.AlbumORM.artist_name)
            & (models.AlbumORM.main_artist_name == models.AlbumMusicORM.main_artist),
        )
        .where(models.AlbumORM.id == album_id)
        .all()
    )
    return res


def db_create_album(db: Session, album: schemas.AlbumModel):
    db_album = models.AlbumORM(**album.model_dump())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album.id


def get_album_id(db: Session, album_id: str):
    album = db.query(models.AlbumORM).where(models.AlbumORM.id == album_id).one()
    return album.name


def delete_album(db: Session, album_name: str):
    row_count = db.query(models.AlbumORM).filter_by(name=album_name).delete()
    db.commit()
    return row_count


def get_album_name(db: Session, album_name: str):
    return db.query(models.AlbumORM).filter_by(name=album_name).one_or_none()
