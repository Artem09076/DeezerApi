"""This module contain app and pages site."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import BADREQUEST, NOTFOUND, tags_metadata
from deezer_api import (get_info_by_id, get_info_track, get_search_result,
                        get_tracklist)

app = FastAPI(openapi_tags=tags_metadata)
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse, tags=['Templates'])
async def read_root(request: Request):
    """Read root.

    Args:
        request (Request): request

    Returns:
        Template response
    """
    return templates.TemplateResponse(request=request, name='home_page.html')


@app.get('/results/', tags=['Templates'])
async def read_results(
    request: Request, search_query: str,
):
    """Read results.

    Args:
        request (Request): request
        search_query (str): search query

    Raises:
        HTTPException: 400 raise when page not found

    Returns:
        Template Response with result page
    """
    search_result = get_search_result(search_query)
    if not (search_result['artists'] and search_result['tracks'] and search_result['albums']):
        raise HTTPException(status_code=BADREQUEST, detail='Nothing came up on your request')
    return templates.TemplateResponse(
        request=request,
        context={
            'result': search_result,
            'query': search_query,
        },
        name='result_page.html',
    )


@app.get('/artist/{artist_id}', tags=['Templates'])
async def read_artist(request: Request, artist_id: int):
    """Read artist.

    Args:
        request (Request): request
        artist_id (int): artist id

    Raises:
        HTTPException: 404 raise if we don't found artist

    Returns:
        Template Response with artist page
    """
    url = f'https://api.deezer.com/artist/{artist_id}/top?limit=15'
    artist_tracks = get_tracklist(url)
    if not artist_tracks:
        raise HTTPException(status_code=NOTFOUND, detail='Atist not found')
    url = f'https://api.deezer.com/artist/{artist_id}'
    fields_name = ('id', 'name', 'picture_medium')
    artist_info = get_info_by_id(url, fields_name)
    return templates.TemplateResponse(
        request=request,
        context={
            'artist_tracks': artist_tracks,
            'artist_info': artist_info,
        },
        name='artist_page.html',
    )


@app.get('/album/{album_id}', tags=['Templates'])
async def read_album(request: Request, album_id: int):
    """Read album.

    Args:
        request (Request): request
        album_id (int): album id

    Raises:
        HTTPException: 404 raise if we not found album

    Returns:
        Template Response with album page
    """
    url = f'https://api.deezer.com/album/{album_id}/tracks'
    album_tracks = get_tracklist(url)
    if not album_tracks:
        raise HTTPException(status_code=NOTFOUND, detail='Atist not found')
    url = f'https://api.deezer.com/album/{album_id}'
    fields_name = ('id', 'title', 'cover_medium')
    album_info = get_info_by_id(url, fields_name)
    return templates.TemplateResponse(
        request=request,
        context={
            'album_tracks': album_tracks,
            'album_info': album_info,
        },
        name='album_tracks.html',
    )


@app.get('/track/{track_id}', tags=['Templates'])
async def read_track(request: Request, track_id: int):
    """Read track.

    Args:
        request (Request): request
        track_id (int): track id

    Returns:
        Template Response with track page
    """
    url = f'https://api.deezer.com/track/{track_id}'
    fields_artist_name = ('id', 'name', 'picture_small')
    fields_album_name = ('id', 'title', 'cover_medium')
    fields_track_name = ('id', 'title', 'preview')
    album_info, artist_info, track_info = get_info_track(url, fields_artist_name, fields_album_name, fields_track_name)
    return templates.TemplateResponse(
        request=request,
        context={
            'track_info': track_info,
            'artist_info': artist_info,
            'album_info': album_info,
        },
        name='track_page.html',
    )
