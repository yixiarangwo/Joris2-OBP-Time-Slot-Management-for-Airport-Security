from dash import dcc

stored = [
    dcc.Store(id = {"section": "intermediate", "type": "parameters", "index": "time-slots"}, storage_type = "session", data = {}),
]
