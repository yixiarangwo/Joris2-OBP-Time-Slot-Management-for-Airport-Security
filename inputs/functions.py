from dash import html, dcc

# Prevent repeating code for making new html divs for time slots input
# Count is used to separate the different time slots for data conversion later
def timeSlotsDiv(flight, count):
    return html.Div(
        id = {"section": "inputs", "type": "div", "index": "time-slots", "flight": flight, "count": count},
        children = [
            html.Label("Time slot capacity",  style = {"marginRight": "1%"}),
            dcc.Input(
                id = {"section": "inputs", "type": "input", "index": "time-slots", "flight": flight, "info": "capacity", "count": count},
                style = {"width": "5%", "marginBottom": "2%", "marginRight": "2%"},
                type = "number",
                value = ""
            ),
            html.Label("Start time",  style = {"marginRight": "1%"}),
            dcc.Input(
                id = {"section": "inputs", "type": "input", "index": "time-slots", "flight": flight, "info": "start-time-hours", "count": count},
                style = {"width": "3%", "marginBottom": "2%", "marginRight": "0.5%"},
                type = "number",
                value = ""
            ),
            html.Label(":", style = {"marginRight": "0.5%"}),
            dcc.Input(
                id = {"section": "inputs", "type": "input", "index": "time-slots", "flight": flight, "info": "start-time-mins", "count": count},
                style = {"width": "3%", "marginBottom": "2%"},
                type = "number",
                value = ""
            ),
        ]
    )


# Convert from Unix time to hours and minutes
def unixToTime24(unixTime):
    # Get hours and minutes
    hours = unixTime // 3600
    minutes = (unixTime % 3600) // 60

    # Format to 24-hour format
    return f"{hours:02d}:{minutes:02}"


# Convert from hours and minutes to Unix
def time24ToUnix(hours, minutes):
    # Check if no time given
    if hours == "" and minutes == "":
        return -1

    # Special case for this project
    if hours == "":
        hours = 0
    if minutes == "":
        minutes = 0
    
    # Convert to unix
    return hours * 3600 + minutes * 60
