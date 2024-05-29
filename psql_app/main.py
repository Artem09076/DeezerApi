from fastapi import APIRouter, status, Depends, HTTPException
from .artist_psql import schemas, crud
from .database import SessionLocal
from sqlalchemy.orm import Session
from .album_psql.schemas import AlbumModel, AlbumRequestModel
from fastapi.templating import Jinja2Templates
from .album_psql.crud import db_create_album, delete_album, get_album_name
from .song_psql.crud import db_create_song, delete_song
from .song_psql.schemas import SongAddModel, SongRequestModel


router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/artists/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ArtistResponseModel,
    tags=["Artists"],
)
async def create_artist(
    artist_request: schemas.ArtistModel, db: Session = Depends(get_db)
):
    new_artist_id = crud.create_artist(db, artist_request)
    return schemas.ArtistResponseModel(id=new_artist_id)


@router.get("/artists/", tags=["Artists"])
async def read_artist(db: Session = Depends(get_db)):
    return crud.get_artists(db)


@router.delete("/artist/", status_code=status.HTTP_204_NO_CONTENT, tags=["Artists"])
async def delete_artist(artist_name: str, db: Session = Depends(get_db)):
    row_count = crud.delete_artist(db, artist_name)
    if not row_count:
        raise HTTPException(status_code=404, detail="Artist not found")


@router.post(
    "/albums",
    status_code=status.HTTP_201_CREATED,
    response_model=AlbumRequestModel,
    tags=["Albums"],
)
async def create_album(album_request: AlbumModel, db: Session = Depends(get_db)):
    new_album_id = db_create_album(db, album_request)
    return {"id": new_album_id}


@router.delete("/albums/", status_code=status.HTTP_204_NO_CONTENT, tags=["Albums"])
async def delete_album_by_name(album_name: str, db: Session = Depends(get_db)):
    row_count = delete_album(db, album_name)
    if not row_count:
        raise HTTPException(status_code=404, detail="Album not found")


@router.get("/albums/", tags=["Albums"])
def get_album_by_name(album_name: str, db: Session = Depends(get_db)):
    res = get_album_name(db, album_name)
    if res is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return res


@router.post(
    "/songs/",
    status_code=status.HTTP_201_CREATED,
    response_model=SongRequestModel,
    tags=["Songs"],
)
async def create_song(song_request: SongAddModel, db: Session = Depends(get_db)):
    id_song = db_create_song(db, song_request)
    return SongRequestModel(id=id_song)


@router.delete("/songs/", status_code=status.HTTP_204_NO_CONTENT, tags=["Songs"])
async def delete_song_by_name(song_name: str, db: Session = Depends(get_db)):
    row_count = delete_song(db, song_name)
    if not row_count:
        raise HTTPException(status_code=404, detail="Song not found")
