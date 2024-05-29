from pydantic import BaseModel, PastDate, UUID4


class AlbumModel(BaseModel):
    name: str
    artist_name: str
    main_artist_name: str
    num_song: int
    cover_link: str
    album_link: str
    date_realise: PastDate

    class Config:
        from_attributes = True


class AlbumRequestModel(BaseModel):
    id: UUID4
