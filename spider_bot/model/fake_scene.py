class FakeScene:
    def __init__(self):
        self.frames = []

    def update(self):
        for frame in self.frames:
            frame.update()
