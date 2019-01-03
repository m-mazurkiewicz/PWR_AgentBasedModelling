class Obstacle:

    def __init__(self, position=(100, 100), size=30.0, color=(1.0, 0.0, 0.0)):
        self.position = position
        self.size = size
        self.color = color
        self.x = (position[0]-size, position[0]+size)
        self.y = (position[1]-size, position[1]+size)
