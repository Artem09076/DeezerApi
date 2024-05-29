from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from psql_app.main import router, templates, get_db
from psql_app.models import Base
from config import engine, tags_metadata
from sqlalchemy.orm import Session
from psql_app.artist_psql.crud import get_artist_album, get_artists, get_artist_by_name
from psql_app.album_psql.crud import get_album_id, get_album_songs
from psql_app.song_psql.crud import get_song, get_result

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router)


@app.get("/", response_class=HTMLResponse, tags=["Templates"])
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home_page.html")


@app.get("/artist/{artist_id}", response_class=HTMLResponse, tags=["Templates"])
async def read_artist_album(
    request: Request, artist_id: str, page: int = 1, db: Session = Depends(get_db)
):
    albums = page * 5
    db_artist_albums = get_artist_album(db, artist_id)
    artist_albums = db_artist_albums[albums - 5 : albums]
    len_albums = len(db_artist_albums)
    count_list = len_albums // 5 if len_albums % 5 == 0 else (len_albums // 5) + 1
    if not db_artist_albums:
        raise HTTPException(status_code=404, detail="Artist not found")
    if page > count_list:
        raise HTTPException(status_code=400, detail="This page not exist")

    return templates.TemplateResponse(
        request=request,
        context={
            "realises": artist_albums,
            "artist_name": artist_id,
            "count_list": count_list,
            "page": page,
        },
        name="artist_realise_page.html",
    )


@app.get("/artist/", response_class=HTMLResponse, tags=["Templates"])
async def read_artists(request: Request, page: int = 1, db: Session = Depends(get_db)):
    artist = page * 5
    db_artists = get_artists(db)
    artists = db_artists[artist - 5 : artist]
    len_artist = len(db_artists)
    count_list = len_artist // 5 if len_artist % 5 == 0 else (len_artist // 5) + 1
    if page > count_list:
        raise HTTPException(status_code=400, detail="This page not exist")

    return templates.TemplateResponse(
        request=request,
        context={"artists": artists, "count_list": count_list, "page": page},
        name="artists_page.html",
    )


@app.get("/albums/{album_id}", response_class=HTMLResponse, tags=["Templates"])
async def read_album_song(
    reqest: Request, album_id: str, db: Session = Depends(get_db)
):
    db_songs = get_album_songs(db, album_id)
    if not db_songs:
        raise HTTPException(status_code=404, detail="Artist not found")
    album_name = get_album_id(db, album_id)
    return templates.TemplateResponse(
        request=reqest,
        context={"songs": db_songs, "album_name": album_name},
        name="album_songs.html",
    )


@app.get("/songs/{song_id}", response_class=HTMLResponse, tags=["Templates"])
async def read_song(request: Request, song_id: str, db: Session = Depends(get_db)):
    db_song = get_song(db, song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    artist = get_artist_by_name(db, db_song.main_artist_name)
    return templates.TemplateResponse(
        request=request,
        context={"song": db_song, "artist": artist},
        name="song_page.html",
    )


@app.get("/search/", response_class=HTMLResponse, tags=["Templates"])
async def read_serch_page(request: Request):
    return templates.TemplateResponse(request=request, name="search_page.html")


@app.get("/results/", tags=["Templates"])
async def read_results(
    request: Request, search_query: str, page: int = 1, db: Session = Depends(get_db)
):
    count_songs = page * 10
    result = get_result(db, search_query)
    if not result:
        raise HTTPException(status_code=400, detail="Nothing came up on your request")
    songs = result[count_songs - 10 : count_songs]
    return templates.TemplateResponse(
        request=request,
        context={
            "songs": songs,
            "count_list": len(result) // 10 if (len(result) // 10) <= 10 else 10,
            "page": page,
            "query": search_query,
        },
        name="result_page.html",
    )
