from pydantic import BaseModel, UUID4


class SongAddModel(BaseModel):
    name: str
    artist_name: str
    main_artist_name: str
    lyrics: str
    song_link: str
    album_name: str

    class Config:
        from_attributes = True


class SongRequestModel(BaseModel):
    id: UUID4
