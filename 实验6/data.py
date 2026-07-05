class Instrument_Data:
    def __init__(self):
        self.repeatibility = []
        self.reoccurbility = []


foreign = Instrument_Data()
domestic = Instrument_Data()

foreign.repeatibility = [14.47999954, 14.47999954, 14.47999954, 14.47999954, 14.48999977,
                         14.5, 14.48999977, 14.48999977, 14.47999954, 14.48999977
                         ]
foreign.reoccurbility = [14.53999996, 14.52000046, 14.61999989, 14.64000034, 14.47999954,
                         14.51000023, 14.53999996, 14.51000023, 14.55000019, 14.60000038
                         ]

domestic.repeatibility = [15.0, 14.93, 14.99, 14.94, 14.93,
                          15.01, 14.92, 14.89, 14.98, 14.95
                          ]
domestic.reoccurbility = [14.96, 14.98, 15.02, 14.77, 14.99,
                          14.94, 14.84, 14.98, 14.95, 15.82
]
