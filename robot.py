from enum import Enum

class Robot:
    def __init__(self, name, robot_type, position):
        self.name = name
        self.type = robot_type
        self.position = position

    def __str__(self):
        return 'R'+str(self.name)

    def __repr__(self):
        return str(self)