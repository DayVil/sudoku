class SlotNumber:
    def __init__(self, num, base, colour=None):
        self.num = str(num)
        self.base = base
        self.colour = colour

    def __str__(self):
        return self.num
