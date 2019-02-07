from enum import Enum

class RobotType(Enum):
    a1 = 'a1'
    a2 = 'a2'
    a3 = 'a3'

class Robot:
    def __init__(self, name, robot_type, position):
        self.name = name
        self.type = robot_type
        self.position = position

    def __str__(self):
        return 'R'+str(self.name)

    def __repr__(self):
        return str(self)