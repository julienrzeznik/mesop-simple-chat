import os

import mesop as me
import mesop.labs as mel

from data_model.state import State

import firebase_admin
from firebase_admin import auth

from components.web.auth.firebase_auth_component import firebase_auth_component

from dotenv import load_dotenv

load_dotenv()



# Avoid re-initializing firebase app (useful for avoiding warning message because of hot reloads).
if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
    default_app = firebase_admin.initialize_app()

def on_auth_changed(e: mel.WebEvent):
    """
    Callback function triggered when the authentication state changes.

    Verifies the Firebase authentication token and updates the user's email in the state.
    Raises an exception if the user is not allowlisted.
    """
    firebaseAuthToken = e.value
    if not firebaseAuthToken:
        me.state(State).email = ""
        return

    decoded_token = auth.verify_id_token(firebaseAuthToken)

    allowlisted_users = os.getenv("ALLOWLISTED_USERS")
    allowlisted_users = allowlisted_users.split(",")

    # You can do an allowlist if needed.
    if decoded_token["email"] not in allowlisted_users:
        raise me.MesopUserException("Invalid user: " + decoded_token["email"])
    me.state(State).email = decoded_token["email"]


def header(header_title):
    """
    Displays the header of the application.
    
    Includes the logo, title, and authentication status.  Also handles navigation to the home page.
    """
    state = me.state(State)

    def navigate_home(e: me.ClickEvent):
        """
        Navigates to the home page and clears the message history.
        """
        me.navigate("/")
        state = me.state(State)
        state.messages = []

    auth_needed = os.getenv("PROTECT_WITH_AUTH")

    if auth_needed == "TRUE":
        with me.box(style=me.Style(display="flex")):
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                if state.email:
                    me.text("Signed in email: " + state.email)
            with me.box():
                firebase_auth_component(on_auth_changed=on_auth_changed)

    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="row",
            justify_content="center",
            align_items="center",
            padding=me.Padding.all(5),
            background="linear-gradient(135deg, #009890 0%, #DF0673 100%) transparent", # Gradient background
            margin=me.Margin.all(40),
            border_radius=16,
            cursor="pointer",
        ),
        on_click=navigate_home,
    ):

        with me.box(
            style=me.Style(
                justify_content="left",
                display="flex",
                padding=me.Padding.all(30),
            )
        ):
            with me.box(
                style=me.Style(
                    width="200px",
                    height="200px",
                    display="flex",
                    background="white",
                    border_radius="50%",  # Circular background for the image
                )
            ):
                me.image(
                    src="https://freesvg.org/img/Logo-Logo.png", # Victoires Capital Humain logo
                    style=me.Style(width="200px", margin=me.Margin(top=0)),
                )

        with me.box(style=me.Style(width="100%")):

            chosen_text = header_title

            me.markdown(
                chosen_text,
                style=me.Style(
                    font_weight="400",
                    font_size=40,
                    font_family="helvetica",
                    color="#fff",  # White text color
                    letter_spacing="0.3px",
                    text_align="center",
                    border_radius=16,
                    padding=me.Padding.all(16),
                    margin=me.Margin.symmetric(horizontal="auto", vertical=20),
                ),
            )

        with me.box(
            style=me.Style(
                justify_content="right",
                display="flex",
                padding=me.Padding.all(30),
            )
        ):
            with me.box(
                style=me.Style(
                    width="200px",
                    height="200px",
                    display="flex",
                    background="white",
                    border_radius="50%", # Circular background for the image
                )
            ):
                me.image(
                    src="https://institute.sfeir.com/wp-content/uploads/2022/12/google-cloud-logo.png", # Google Cloud logo
                    style=me.Style(width="150px", margin=me.Margin(top=40, left=30)),
                )