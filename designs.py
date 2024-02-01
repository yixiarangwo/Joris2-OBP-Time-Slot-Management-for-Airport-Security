import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Default submit button
def submitButton(name = "", icon = "", id = {}, buttonStyle = {}, width = 25, disabled = False):
    return dmc.Button(
        name,
        rightIcon = DashIconify(icon = icon, width = width),
        id = id,
        style = {
            "height": "2.5rem",
            "textAlign": "center",
            "font-size": "16px",
            "font-weight": "bold",
            "color": "white",
            "margin": 0,
        } | buttonStyle,
        variant = "outline",
        disabled = disabled,
    )
