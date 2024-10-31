import json


class Wave:
    def __init__(self, stage, wave_number):
        self.stage = stage
        self.wave_number = wave_number
        self.enemies = json.load()