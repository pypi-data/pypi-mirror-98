class windFarm:
    def __init__(self, name):
        self.name = name
    def test(self):
        return self.name

windFarm=windFarm("Curslack")
print(windFarm.test())