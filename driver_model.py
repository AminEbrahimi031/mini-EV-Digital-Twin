class Driver:
    def __init__(self, mode="normal"):
        self.mode = mode.lower()

    def get_throttle(self):
        if self.mode == "eco":
            return 0.3
        elif self.mode == "normal":
            return 0.5
        elif self.mode == "aggressive":
            return 0.8
        else:
            return 0.5