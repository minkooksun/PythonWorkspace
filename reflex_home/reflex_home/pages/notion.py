import reflex as rx 
from reflex_home.notion_state import  NotionState
from reflex_home.components import chat, navbar
from reflex_home.models import Movie

def show_movie(movie: Movie):
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.row_header_cell(movie.title),
        rx.table.cell(movie.id),
        rx.table.cell(movie.thumbnail),
        align="center",
    )

@rx.page(route="/notion")
def notion():
    """The notion page.""" 
    return rx.chakra.vstack(
        navbar(),
         rx.center( 
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Customers", size="8"),
                        rx.button(
                            rx.icon(tag="plus"),
                            on_click=NotionState.get_movies,
                            size="3",
                        ),
                        align="center",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("title"),
                                rx.table.column_header_cell("id"),
                                rx.table.column_header_cell("thumbnail"), 
                            )
                        ),
                        rx.table.body(rx.foreach(NotionState.movies, show_movie)),  # type: ignore
                        variant="surface",
                        bg="#F7FAFC ",
                        border="1px solid #ddd",
                        border_radius="10px",
                    ),
                    align_items="left",
                    padding_top="7em",
                ), 
                padding_top="4em",
            ),
            padding="1em",
        ),
    ) 
