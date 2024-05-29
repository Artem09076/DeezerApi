from sqlalchemy.orm import Session

from .. import models
from . import schemas


def create_artist(db: Session, artist: schemas.ArtistModel):
    db_artist = models.ArtistORM(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist.id


def get_artist_album(db: Session, artist_id: str):
    res = (
        db.query(models.AlbumORM)
        .join(
            models.ArtistORM, models.ArtistORM.name == models.AlbumORM.main_artist_name
        )
        .where(models.ArtistORM.id == artist_id)
        .order_by(models.AlbumORM.date_realise.desc())
        .all()
    )
    return res


def get_artist_by_name(db: Session, artist_name: str):
    return db.query(models.ArtistORM).filter_by(name=artist_name).one_or_none()


def get_artists(db: Session):
    res = []
    for artist in db.query(models.ArtistORM).all():
        albums = db.query(models.AlbumORM).filter_by(main_artist_name=artist.name).all()
        if albums:
            res.append(artist)
    return res


def delete_artist(db: Session, artist_name: str):
    row_cont = db.query(models.ArtistORM).filter_by(name=artist_name).delete()
    db.commit()
    return row_cont
