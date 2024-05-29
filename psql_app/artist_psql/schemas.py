from pydantic import BaseModel, UUID4


class ArtistModel(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ArtistResponseModel(BaseModel):
    id: UUID4


class AlbumMusicModel(BaseModel):
    artist_name: str
    main_artist: str
    album_name: str
    song_name: str
