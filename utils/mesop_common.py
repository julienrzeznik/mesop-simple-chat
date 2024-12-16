import mesop as me

STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap",
    "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.css",
]

ROOT_BOX_STYLE = me.Style(
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
    background="white",
)


ALLOWED_SCRIPTS_SRCS = [
    "*.google.com",
    "https://www.gstatic.com",
    "https://cdn.jsdelivr.net",
    "https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js",
]

ALLOWED_CONNECT_SRCS = [
    "*.googleapis.com"
]