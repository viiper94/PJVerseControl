class Projector:
    def __init__(self, index, port):
        self.id = index
        self.port = port

        self.power_status = None
        self.blank_status = None
        self.freeze_status = None
        self.source = None
        self.lamp_hour = None
