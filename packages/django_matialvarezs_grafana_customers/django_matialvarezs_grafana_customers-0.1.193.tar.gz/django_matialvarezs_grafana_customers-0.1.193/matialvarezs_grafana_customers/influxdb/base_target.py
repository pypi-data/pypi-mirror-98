def get_target_panel(measurement,field,**options):
    alias = options.get("alias","")
    refId = options.get("refId",None)
    return {
        "alias":alias,
        "groupBy": [],
        "measurement": measurement,
        "orderByTime": "ASC",
        "policy": "default",
        "refId": refId,
        "resultFormat": "time_series",
        "select": [
            [
                {
                    "params": [
                        field
                    ],
                    "type": "field"
                }
            ]
        ],
        "tags": []
    }
