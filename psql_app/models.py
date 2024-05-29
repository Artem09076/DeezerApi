"""This module contain models."""
from datetime import date
from uuid import uuid4

from sqlalchemy import (CheckConstraint, Date, ForeignKey,
                        ForeignKeyConstraint, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Empty class Base.

    Args:
        DeclarativeBase: declarative base
    """

    pass


def generetic_uuid4():
    """UUID to str.

    Returns:
        str version object UUID4
    """
    return str(uuid4())


class UUIDMixin:
    """Mixin with id fields."""

    id: Mapped[str] = mapped_column(default=generetic_uuid4)


class ArtistORM(UUIDMixin, Base):
    """Artist model ORM.

    Args:
        UUIDMixin: mixin with id fields
        Base: model for create this model in db
    """

    __tablename__ = 'artist'
    name: Mapped[str] = mapped_column(String(300), primary_key=True)


class AlbumORM(UUIDMixin, Base):
    """Album model ORM.

    Args:
        UUIDMixin: mixin with id fields
        Base: model for create this model in db
    """

    __tablename__ = 'album'

    name: Mapped[str] = mapped_column(String(500), primary_key=True)

    artist_name: Mapped[str] = mapped_column(
        String(300), ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
    )
    main_artist_name: Mapped[str] = mapped_column(
        String(300),
        ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )

    num_song: Mapped[int] = mapped_column(Integer, CheckConstraint('num_song > 0'))
    cover_link: Mapped[str] = mapped_column(String(100), nullable=True)
    album_link: Mapped[str] = mapped_column(String(100))
    date_realise: Mapped[date] = mapped_column(
        Date, CheckConstraint('date_realise <= CURRENT_DATE'),
    )

    __table_args__ = (
        UniqueConstraint(
            'artist_name', 'main_artist_name', 'name', name='artist_name_album_unique',
        ),
    )


class SongORM(UUIDMixin, Base):
    """Song model ORM.

    Args:
        UUIDMixin: mixin with id fields
        Base: model for create this model in db
    """

    __tablename__ = 'song'

    name: Mapped[str] = mapped_column(String(300), primary_key=True)

    artist_name: Mapped[str] = mapped_column(
        String(1000),
        ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )
    main_artist_name: Mapped[str] = mapped_column(
        String(300),
        ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )

    lyrics: Mapped[str] = mapped_column(String(6000), nullable=True)
    song_link: Mapped[str] = mapped_column(String(100))

    __table_args__ = (
        UniqueConstraint(
            'artist_name', 'main_artist_name', 'name', name='artist_name_song_unique',
        ),
    )


class AlbumMusicORM(UUIDMixin, Base):
    """Model ORM for create relation between other models.

    Args:
        UUIDMixin: mixin with id fields
        Base: model for create this model in db
    """

    __tablename__ = 'album_music'

    artist_name: Mapped[str] = mapped_column(
        String(300),
        ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )
    main_artist: Mapped[str] = mapped_column(
        String(300),
        ForeignKey('artist.name', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )

    album_name = mapped_column(String(300), primary_key=True)
    song_name = mapped_column(String(300), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['artist_name', 'song_name', 'main_artist'],
            ['song.artist_name', 'song.name', 'song.main_artist_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        ForeignKeyConstraint(
            ['artist_name', 'album_name', 'main_artist'],
            ['album.artist_name', 'album.name', 'album.main_artist_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
    )
