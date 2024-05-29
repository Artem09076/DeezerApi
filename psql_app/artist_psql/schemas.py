"""This module contain artist module for any action."""
from pydantic import UUID4, BaseModel


class ArtistModel(BaseModel):
    """Artist model."""

    name: str

    class Config:
        """Config class for ArtistModel."""

        from_attributes = True


class ArtistResponseModel(BaseModel):
    """Artist model for request."""

    id: UUID4


class AlbumMusicModel(BaseModel):
    """AlbumMusic model."""

    artist_name: str
    main_artist: str
    album_name: str
    song_name: str
