"""This module contain function for add realise."""
from datetime import date

import requests
from lyricsgenius import Genius
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import check_exists_album_in_db, check_relation, insert_new_artist
from discography_artist import get_album_track, get_discography
from psql_app.config import GENIUSTOKEN, SONGRIGHTBROAD, engine
from psql_app.models import AlbumMusicORM, AlbumORM, ArtistORM, SongORM


def get_lyrics(name_song: str, artist_name: str) -> str | None:
    """Get lyrics song.

    Args:
        name_song (str): song name
        artist_name (str): artist name

    Returns:
        str | None: lyrics song
    """
    genius = Genius(GENIUSTOKEN, remove_section_headers=True)
    try:
        song = genius.search_song(name_song, artist_name)
    except requests.exceptions.Timeout:
        return None
    if song is None:
        return None
    if artist_name not in song.artist:
        return None
    return '\n'.join(song.lyrics.split('\n')[1:-1])[:SONGRIGHTBROAD]


def realise_create(artist_name: str) -> None:
    """Create realise.

    Args:
        artist_name (str): artist name
    """
    discography = get_discography(artist_name)
    for (
        name_realise,
        type_realise,
        realise_date,
        realise_link,
        cover_link,
        api_link,
        artist_list,
        total_tracks,
    ) in discography:
        insert_new_artist(artist_list)
        if type_realise == 'single':
            realise_create_for_single(
                name_realise, realise_date, realise_link, cover_link, artist_list,
            )
        else:
            realise_create_for_album(
                name_realise,
                realise_date,
                cover_link,
                realise_link,
                api_link,
                artist_list,
                total_tracks,
            )


def realise_create_for_single(
    name_realise: str,
    realise_date: date,
    realise_link: str,
    cover_link: str,
    artist_list: list[str],
):
    """Create models for singles.

    Args:
        name_realise (str): realise name
        realise_date (date): date realise
        realise_link (str): realise ink
        cover_link (str): cover link
        artist_list (list[str]): list artist
    """
    main_artist = artist_list[0]
    artists = artist_list[1] if len(artist_list) >= 2 else main_artist
    rel = check_relation(
        name_realise, name_realise, artist_name=artists, main_artist=main_artist,
    )
    if not rel:
        return
    with Session(engine) as session:
        song = SongORM(
            name=name_realise,
            artist_name=artists,
            main_artist_name=main_artist,
            song_link=realise_link,
            lyrics=get_lyrics(name_realise, main_artist),
        )

        album = AlbumORM(
            name=name_realise,
            artist_name=artists,
            main_artist_name=main_artist,
            num_song=1,
            cover_link=cover_link,
            album_link=realise_link,
            date_realise=realise_date,
        )
        session.add_all([song, album])
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return
        session.refresh(song)
        session.refresh(album)
        album_music = AlbumMusicORM(
            artist_name=artists,
            main_artist=main_artist,
            album_name=album.name,
            song_name=song.name,
        )
        session.add(album_music)
        session.commit()


def realise_create_for_album(
    name_realise: str,
    realise_date: date,
    cover_link: str,
    realise_link: str,
    api_link: str,
    artist_list: list[str],
    total_tracks: int,
):
    """Create models for albums.

    Args:
        name_realise (str): realise name
        realise_date (date): date realise
        cover_link (str): cover link
        realise_link (str): realise link
        api_link (str): link for album track
        artist_list (list[str]): artist list
        total_tracks (int): total tracks
    """
    artist_name = artist_list[1] if len(artist_list) >= 2 else artist_list[0]
    main_artist_name = artist_list[0]
    if not check_exists_album_in_db(
        album_name=name_realise,
        main_artist_name=main_artist_name,
        artist_name=artist_name,
    ):
        return

    album = AlbumORM(
        name=name_realise,
        artist_name=artist_name,
        main_artist_name=main_artist_name,
        num_song=total_tracks,
        cover_link=cover_link,
        album_link=realise_link,
        date_realise=realise_date,
    )
    with Session(engine) as session:
        session.add(album)
        session.commit()
        session.refresh(album)

        for song_name, song_link, artist_song_list in get_album_track(api_link):
            insert_new_artist(artist_song_list)
            existing_song = (
                session.query(SongORM)
                .filter_by(
                    name=song_name,
                    artist_name=artist_name,
                    main_artist_name=main_artist_name,
                )
                .one_or_none()
            )
            if not existing_song:
                song = SongORM(
                    name=song_name,
                    artist_name=artist_name,
                    main_artist_name=main_artist_name,
                    lyrics=get_lyrics(song_name, main_artist_name),
                    song_link=song_link,
                )
                session.add(song)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    continue
                inserted_song = (
                    session.query(SongORM)
                    .filter_by(
                        name=song_name,
                        artist_name=artist_name,
                        main_artist_name=main_artist_name,
                    )
                    .one_or_none()
                )
                if inserted_song:
                    album_music = AlbumMusicORM(
                        artist_name=artist_name,
                        main_artist=main_artist_name,
                        album_name=name_realise,
                        song_name=inserted_song.name,
                    )
                    session.add(album_music)
                    try:
                        session.commit()
                    except IntegrityError:
                        session.rollback()


def create_null_album_artist():
    """Create realise for whose non have any albums."""
    with Session(engine) as session:
        artists = session.query(ArtistORM).all()
        for artist in artists:
            albums = (
                session.query(AlbumORM).filter_by(main_artist_name=artist.name).all()
            )
            if not albums:
                realise_create(artist.name)
