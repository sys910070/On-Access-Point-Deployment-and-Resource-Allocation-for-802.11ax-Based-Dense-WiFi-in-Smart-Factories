from enum import(IntEnum, unique)

@unique
class State(IntEnum):
    init = 1
    active = 2
    underpopulated = 3
    idle = 4

class ap:
    def __init__(self, x, y, power, channel, capacity, id, type_ap, timer, state):
        self.x = x
        self.y = y
        self.power = power
        self.channel = channel
        self.user = []
        self.capacity = capacity
        self.id = id
        self.type = type_ap
        self.timer = timer
        self.state = state
    
    def adduser(self, user):
        self.user.append(user)

    def association():
        pass

    def check_state_change(self, t, timer, user, lowerbound):
        if timer == 0 or t%30 == 0 or len(user)< lowerbound: 
            return True

    def action():
        pass
    
    def update():
        pass


    self.adduser(2)

