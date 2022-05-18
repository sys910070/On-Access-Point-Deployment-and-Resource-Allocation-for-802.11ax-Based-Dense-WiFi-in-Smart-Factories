from enum import(IntEnum, unique)

@unique
class State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4

class device:
    def _init_(self, x, y, vx, vy, power, channel, id, type_device, dis, state):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.power = power
        self.channel = channel
        self.id = id
        self.type = type_device
        self.dis = dis
        self.state = state

    def move(x, vx, y, vy):
        x = x + vx
        y = y + vy

    def state_change():
        pass