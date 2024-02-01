from dash import dcc

stored = [
    dcc.Store(id = {"section": "intermediate", "type": "parameters", "index": "time-slots"},              storage_type = "session", data = {}),
    dcc.Store(id = {"section": "intermediate", "type": "tracking",   "index": "prev-recom-button-state"}, storage_type = "session", data = False),
    dcc.Store(id = {"section": "intermediate", "type": "parameters", "index": "lane-cap"},                storage_type = "session", data = 40),
    
    # Intervals for notifying the user of saving time slots
    dcc.Interval(
        id = { "section": "inputs", "type": "interval", "index": "save-time-slots" },
        interval = 2000,
        disabled = True,
    ),

    # Intervals for notifying the user of loading time slots
    dcc.Interval(
        id = { "section": "inputs", "type": "interval", "index": "load-time-slots" },
        interval = 2000,
        disabled = True,
    ),
]
