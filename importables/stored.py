from dash import dcc

stored = [
    # Intermediate values to store data, service time distribution, and parameters
    dcc.Store(id = {"section": "intermediate", "type": "dataframe", "index": "arrivals"},     storage_type = "session", data = {}),
    dcc.Store(id = {"section": "intermediate", "type": "dataframe", "index": "flights"},      storage_type = "session", data = {}),
    dcc.Store(id = {"section": "intermediate", "type": "dataframe", "index": "lanes"},        storage_type = "session", data = {}),
    dcc.Store(id = {"section": "intermediate", "type": "dataframe", "index": "service-test"}, storage_type = "session", data = {}),
    
    dcc.Store(id = {"section": "intermediate", "type": "parameters", "index": "sample-info"}, storage_type = "session",
              data = {"latex": r"\exp(-\frac{\left| x \right|}{20})", "lower": 0, "upper": None, 
                      "sigma": 10, "lowerExpansion": 20, "upperExpansion": 2, "initial": ""}),
    dcc.Store(id = {"section": "intermediate", "type": "parameters", "index": "test-info"},   storage_type = "session", data = {}),

    # Intervals for notifying the user
    dcc.Interval(
        id = { "section": "importables", "type": "interval", "index": "arrivals" },
        interval = 2000,
        disabled = True,
    ),
    dcc.Interval(
        id = { "section": "importables", "type": "interval", "index": "flights" },
        interval = 2000,
        disabled = True,
    ),
    dcc.Interval(
        id = { "section": "importables", "type": "interval", "index": "lanes" },
        interval = 2000,
        disabled = True,
    ),
]
