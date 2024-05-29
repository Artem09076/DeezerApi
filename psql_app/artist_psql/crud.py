"""This module include any action with db."""
from sqlalchemy.orm import Session

from .. import models
from . import schemas


def create_artist(db: Session, artist: schemas.ArtistModel):
    """Create artist.

    Args:
        db (Session): session db
        artist (schemas.ArtistModel): model for create new artist

    Returns:
        id created model
    """
    db_artist = models.ArtistORM(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist.id


def get_artist_album(db: Session, artist_id: str):
    """Get artist album.

    Args:
        db (Session): session db
        artist_id (str): artist id

    Returns:
        list with albums artist
    """
    return (
        db.query(models.AlbumORM)
        .join(
            models.ArtistORM, models.ArtistORM.name == models.AlbumORM.main_artist_name,
        )
        .where(models.ArtistORM.id == artist_id)
        .order_by(models.AlbumORM.date_realise.desc())
        .all()
    )


def get_artist_by_name(db: Session, artist_name: str):
    """Get artist by name.

    Args:
        db (Session): db session
        artist_name (str): artist naem

    Returns:
        Artist model
    """
    return db.query(models.ArtistORM).filter_by(name=artist_name).one_or_none()


def get_artists(db: Session):
    """Get all  artists.

    Args:
        db (Session): session db

    Returns:
        All artist with any albums
    """
    res = []
    for artist in db.query(models.ArtistORM).all():
        albums = db.query(models.AlbumORM).filter_by(main_artist_name=artist.name).all()
        if albums:
            res.append(artist)
    return res


def delete_artist(db: Session, artist_name: str):
    """Delete artist by name.

    Args:
        db (Session): db session
        artist_name (str): artist name

    Returns:
        count artists was deleted
    """
    row_cont = db.query(models.ArtistORM).filter_by(name=artist_name).delete()
    db.commit()
    return row_cont
