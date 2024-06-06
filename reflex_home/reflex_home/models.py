import reflex as rx 

class Movie(rx.Model, table=True):  # type: ignore
    """The movie model."""

    title: str 
    thumbnail: str 
    video_id:str