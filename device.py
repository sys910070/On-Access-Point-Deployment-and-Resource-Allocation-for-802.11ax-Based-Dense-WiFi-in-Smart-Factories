from enum import(IntEnum, unique)

@unique
class State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4

class DEVICE:
    def _init_(self, x, y, vx, vy, id, type_device):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.power = 0
        self.channel = 0
        self.id = id
        self.type = type_device
        self.state = State.init

    def move(x, vx, y, vy):
        x = x + vx
        y = y + vy
    

    def state_change():
        pass