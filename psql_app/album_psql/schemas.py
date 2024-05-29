"""This module contain album module for any action."""
from pydantic import BaseModel, PastDate


class AlbumModel(BaseModel):
    """Album Model."""

    name: str
    artist_name: str
    main_artist_name: str
    num_song: int
    cover_link: str
    album_link: str
    date_realise: PastDate

    class Config:
        """Config class for AlbumModel."""

        from_attributes = True


class AlbumRequestModel(BaseModel):
    """Album model for request."""

    id: str
