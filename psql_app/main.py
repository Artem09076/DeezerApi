"""This module contain request for orm."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, sessionmaker

from .album_psql.crud import db_create_album, delete_album, get_album_name
from .album_psql.schemas import AlbumModel, AlbumRequestModel
from .artist_psql import crud, schemas
from .config import NOTFOUND, engine
from .song_psql.crud import db_create_song, delete_song
from .song_psql.schemas import SongAddModel, SongRequestModel

SessionLocal = sessionmaker(bind=engine, autoflush=False)

router = APIRouter()

templates = Jinja2Templates(directory='templates')


def get_db():
    """Get db.

    Yields:
        Session: db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dep_db = Depends(get_db)


@router.post(
    '/artists/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ArtistResponseModel,
    tags=['Artists'],
)
async def create_artist(
    artist_request: schemas.ArtistModel, db: Session = dep_db,
):
    """Post request for model Artist.

    Args:
        artist_request (schemas.ArtistModel): artist request
        db (Session): session db. Defaults to dep_db.

    Returns:
        id created artist
    """
    new_artist_id = crud.create_artist(db, artist_request)
    return schemas.ArtistResponseModel(id=new_artist_id)


@router.get('/artists/', tags=['Artists'])
async def read_artist(db: Session = dep_db):
    """Get request for artist.

    Args:
        db (Session): session db. Defaults to dep_db.

    Returns:
        list with artists
    """
    return crud.get_artists(db)


@router.delete('/artist/', status_code=status.HTTP_204_NO_CONTENT, tags=['Artists'])
async def delete_artist(artist_name: str, db: Session = dep_db):
    """Delete request for artist by name.

    Args:
        artist_name (str): artist name
        db (Session): session db. Defaults to dep_db.

    Raises:
        HTTPException: 404 when artist was not found
    """
    row_count = crud.delete_artist(db, artist_name)
    if not row_count:
        raise HTTPException(status_code=NOTFOUND, detail='Artist not found')


@router.post(
    '/albums',
    status_code=status.HTTP_201_CREATED,
    response_model=AlbumRequestModel,
    tags=['Albums'],
)
async def create_album(album_request: AlbumModel, db: Session = dep_db):
    """Post request for model album.

    Args:
        album_request (AlbumModel): album request
        db (Session): session db. Defaults to dep_db.

    Returns:
        id created album
    """
    new_album_id = db_create_album(db, album_request)
    return AlbumRequestModel(id=new_album_id)


@router.delete('/albums/', status_code=status.HTTP_204_NO_CONTENT, tags=['Albums'])
async def delete_album_by_name(album_name: str, db: Session = dep_db):
    """Delete request for album model by album name.

    Args:
        album_name (str): album name
        db (Session): session db. Defaults to dep_db.

    Raises:
        HTTPException: 404 when album was not found
    """
    row_count = delete_album(db, album_name)
    if not row_count:
        raise HTTPException(status_code=NOTFOUND, detail='Album not found')


@router.get('/albums/', tags=['Albums'])
def get_album_by_name(album_name: str, db: Session = dep_db):
    """Get request album model by name.

    Args:
        album_name (str): album name
        db (Session): session db. Defaults to dep_db.

    Raises:
        HTTPException: 404 when album was not found

    Returns:
        Album models
    """
    res = get_album_name(db, album_name)
    if res is None:
        raise HTTPException(status_code=NOTFOUND, detail='Album not found')
    return res


@router.post(
    '/songs/',
    status_code=status.HTTP_201_CREATED,
    response_model=SongRequestModel,
    tags=['Songs'],
)
async def create_song(song_request: SongAddModel, db: Session = dep_db):
    """Create request for song model.

    Args:
        song_request (SongAddModel): song request
        db (Session): session db. Defaults to dep_db.

    Returns:
        id created song
    """
    id_song = db_create_song(db, song_request)
    return SongRequestModel(id=id_song)


@router.delete('/songs/', status_code=status.HTTP_204_NO_CONTENT, tags=['Songs'])
async def delete_song_by_name(song_name: str, db: Session = dep_db):
    """Delete request for song model.

    Args:
        song_name (str): song name
        db (Session): session db. Defaults to dep_db.

    Raises:
        HTTPException: 404 when song was not found
    """
    row_count = delete_song(db, song_name)
    if not row_count:
        raise HTTPException(status_code=NOTFOUND, detail='Song not found')
