from lyricsgenius import Genius
from sqlalchemy.orm import Session

from config import GENIUSTOKEN, engine
from db import insert_new_artist, check_relation, check_exists_album_in_db
from discography_artist import get_discography, get_album_track
from psql_app.models import AlbumORM, AlbumMusicORM, SongORM, ArtistORM
from datetime import date
import requests
from sqlalchemy.exc import IntegrityError


def get_lyrics(name_song: str, artist_name: str) -> str:
    try:
        genius = Genius(GENIUSTOKEN, remove_section_headers=True)
        song = genius.search_song(name_song, artist_name)
    except requests.exceptions.Timeout:
        print(f"When searched lyrics {name_song} by {artist_name} was raised timeout")
        return
    if song is None:
        return
    if artist_name not in song.artist:
        return
    return "\n".join(song.lyrics.split("\n")[1:-1])[:6000]


def realise_create(artist_name: str) -> list:
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
        if type_realise == "single":
            realise_create_for_single(
                name_realise, realise_date, realise_link, cover_link, artist_list
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

    artists = artist_list[1] if len(artist_list) >= 2 else artist_list[0]
    rel = check_relation(
        name_realise, name_realise, artist_name=artists, main_artist=artist_list[0]
    )
    if not rel:
        return
    with Session(engine) as session:
        song = SongORM(
            name=name_realise,
            artist_name=artists,
            main_artist_name=artist_list[0],
            song_link=realise_link,
            lyrics=get_lyrics(name_realise, artist_list[0]),
        )

        album = AlbumORM(
            name=name_realise,
            artist_name=artists,
            main_artist_name=artist_list[0],
            num_song=1,
            cover_link=cover_link,
            album_link=realise_link,
            date_realise=realise_date,
        )
        session.add_all([song, album])
        try:
            session.commit()
            session.refresh(song)
            session.refresh(album)
        except IntegrityError:
            print(f"Can`t add song {song.name}")
            session.rollback()
            return

        album_music = AlbumMusicORM(
            artist_name=artists,
            main_artist=artist_list[0],
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
    artist_name = artist_list[1] if len(artist_list) >= 2 else artist_list[0]
    main_artist_name = artist_list[0]
    if not check_exists_album_in_db(
        album_name=name_realise,
        album_main_artist_name=main_artist_name,
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
                    print(f"We can`t add {song_name}")
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
    with Session(engine) as session:
        artists = session.query(ArtistORM).all()
        for artist in artists:
            albums = (
                session.query(AlbumORM).filter_by(main_artist_name=artist.name).all()
            )
            if not albums:
                realise_create(artist.name)


