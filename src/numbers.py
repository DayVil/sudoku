class SlotNumber:
    def __init__(self, num, base, colour=None):
        self.num = num
        self.base = base
        self.colour = colour

    def __str__(self):
        return self.num
