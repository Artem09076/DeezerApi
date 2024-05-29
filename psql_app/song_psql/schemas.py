"""This module contain song module for any action."""
from pydantic import UUID4, BaseModel


class SongAddModel(BaseModel):
    """Model for add song in db."""

    name: str
    artist_name: str
    main_artist_name: str
    lyrics: str
    song_link: str
    album_name: str

    class Config:
        """Config class for SongAddModel."""

        from_attributes = True


class SongRequestModel(BaseModel):
    """Model for return after create song."""

    id: UUID4
