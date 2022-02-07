class MenuDateException(Exception):
    def __init__(self, msg):
        self.message = msg
