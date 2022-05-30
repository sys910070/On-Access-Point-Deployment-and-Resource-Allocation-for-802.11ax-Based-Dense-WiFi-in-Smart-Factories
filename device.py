from enum import(IntEnum, unique)

@unique
class State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4

class DEVICE:
    def __init__(self, x, y, vx, vy, id, type_device):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.power = 0
        self.channel = 0
        self.id = id
        self.type = type_device
        self.state = State.init
        self.ap = 0

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    
    def state_change():
        pass