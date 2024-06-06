import reflex as rx

from .pages.index import index
from .pages.notion import notion

 
# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)

app.add_page(index, route="/")
app.add_page(notion, route="/notion")