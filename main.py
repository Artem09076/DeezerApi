"""This module contain app and pages site."""
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from psql_app.album_psql.crud import get_album_id, get_album_songs
from psql_app.artist_psql.crud import (get_artist_album, get_artist_by_name,
                                       get_artists)
from psql_app.config import BADREQUEST, NOTFOUND, engine, tags_metadata
from psql_app.main import get_db, router, templates
from psql_app.models import Base
from psql_app.song_psql.crud import get_result, get_song

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router)


@app.get('/', response_class=HTMLResponse, tags=['Templates'])
async def read_root(request: Request):
    """Read root.

    Args:
        request (Request): request

    Returns:
        Template response
    """
    return templates.TemplateResponse(request=request, name='home_page.html')


@app.get('/artist/{artist_id}', response_class=HTMLResponse, tags=['Templates'])
async def read_artist_album(
    request: Request, artist_id: str, page: int = 1, db: Session = Depends(get_db),
):
    """Read page albums artist.

    Args:
        request (Request): request
        artist_id (str): id artist
        page (int): Num of page. Defaults to 1.
        db (Session): DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 raise when page not found
        HTTPException: 404 raise when artist not found

    Returns:
        Template response with albums artist page
    """
    albums = page * 5
    db_artist_albums = get_artist_album(db, artist_id)
    artist_albums = db_artist_albums[albums - 5:albums]
    len_albums = len(db_artist_albums)
    count_list = len_albums // 5 if len_albums % 5 == 0 else (len_albums // 5) + 1
    if not db_artist_albums:
        raise HTTPException(status_code=NOTFOUND, detail='Artist not found')
    if page > count_list:
        raise HTTPException(status_code=BADREQUEST, detail='This page not exist')

    return templates.TemplateResponse(
        request=request,
        context={
            'realises': artist_albums,
            'artist_name': artist_id,
            'count_list': count_list,
            'page': page,
        },
        name='artist_realise_page.html',
    )


@app.get('/artist/', response_class=HTMLResponse, tags=['Templates'])
async def read_artists(request: Request, page: int = 1, db: Session = Depends(get_db)):
    """Read artists page.

    Args:
        request (Request): _description_
        page (int): Num of page. Defaults to 1.
        db (Session): DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 raise when page not found

    Returns:
        Template Response with artists page
    """
    artist = page * 5
    db_artists = get_artists(db)
    artists = db_artists[artist - 5:artist]
    len_artist = len(db_artists)
    count_list = len_artist // 5 if len_artist % 5 == 0 else (len_artist // 5) + 1
    if page > count_list:
        raise HTTPException(status_code=BADREQUEST, detail='This page not exist')

    return templates.TemplateResponse(
        request=request,
        context={'artists': artists, 'count_list': count_list, 'page': page},
        name='artists_page.html',
    )


@app.get('/albums/{album_id}', response_class=HTMLResponse, tags=['Templates'])
async def read_album_song(
    request: Request, album_id: str, db: Session = Depends(get_db),
):
    """Read albums song.

    Args:
        request (Request): request
        album_id (str): id album
        db (Session): DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 raise when Album not found

    Returns:
        Template Response with album songs page
    """
    db_songs = get_album_songs(db, album_id)
    if not db_songs:
        raise HTTPException(status_code=NOTFOUND, detail='Album not found')
    album_name = get_album_id(db, album_id)
    return templates.TemplateResponse(
        request=request,
        context={'songs': db_songs, 'album_name': album_name},
        name='album_songs.html',
    )


@app.get('/songs/{song_id}', response_class=HTMLResponse, tags=['Templates'])
async def read_song(request: Request, song_id: str, db: Session = Depends(get_db)):
    """Read song page.

    Args:
        request (Request): request
        song_id (str): id song
        db (Session): DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 raise when song not found

    Returns:
        Template Response with song page
    """
    db_song = get_song(db, song_id)
    if db_song is None:
        raise HTTPException(status_code=NOTFOUND, detail='Song not found')
    artist = get_artist_by_name(db, db_song.main_artist_name)
    return templates.TemplateResponse(
        request=request,
        context={'song': db_song, 'artist': artist},
        name='song_page.html',
    )


@app.get('/search/', response_class=HTMLResponse, tags=['Templates'])
async def read_serch_page(request: Request):
    """Read serch page.

    Args:
        request (Request): request

    Returns:
        Template Response with search page
    """
    return templates.TemplateResponse(request=request, name='search_page.html')


@app.get('/results/', tags=['Templates'])
async def read_results(
    request: Request, search_query: str, page: int = 1, db: Session = Depends(get_db),
):
    """Read results.

    Args:
        request (Request): request
        search_query (str): search query
        page (int): page num. Defaults to 1.
        db (Session): DB. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 raise when page not found

    Returns:
        Template Response with result page
    """
    count_songs = page * 10
    db_result = get_result(db, search_query)
    if not db_result:
        raise HTTPException(status_code=BADREQUEST, detail='Nothing came up on your request')
    songs = db_result[count_songs - 10:count_songs]
    return templates.TemplateResponse(
        request=request,
        context={
            'songs': songs,
            'count_list': len(db_result) // 10 if (len(db_result) // 10) <= 10 else 10,
            'page': page,
            'query': search_query,
        },
        name='result_page.html',
    )
