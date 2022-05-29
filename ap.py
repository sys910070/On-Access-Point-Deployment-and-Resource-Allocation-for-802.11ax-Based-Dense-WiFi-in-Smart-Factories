from enum import(IntEnum, unique)
from parameter import*
from utils import distance

#all mathematical model constant  
GTX = 4 #sender antenna gain
GRX = 4 #receiver antenna gain
ETA = 4 #path-loss exponent
CHI = 5 #standard deviation association with the degree of shadow fading
P_REF = 46 #the path loss at a reference distance(1m)
THETA_DECODE = -68 #threshold of decode signal strength
THETA_INTERFERENCE = -77 #threshold of interference signal strength

@unique
class State(IntEnum):
    init = 1
    active = 2
    underpopulated = 3
    idle = 4

class AP:
    def __init__(self, x, y, capacity, id, type_ap):
        self.x = x
        self.y = y
        self.power = 0
        self.channel = 0
        self.user = []
        self.capacity = capacity
        self.id = id
        self.type = type_ap
        self.timer = 0
        self.state = State.init
        self.cci = 0
        self.neighbor = []
        self.interference_range = 0
        self.communication_range = 0

    def power_change(self, power):
        self.power = power
        self.interference_range = 10**((power+GTX+GRX-P_REF-CHI-THETA_INTERFERENCE)/(10*ETA))
        self.communication_range = 10**((power+GTX+GRX-P_REF-CHI-THETA_DECODE)/(10*ETA))

    def add_neighbor_ap(self, ap_list):
        for ap in ap_list:
            if self.interference_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self:
                self.neighbor.append(ap.id)

    def adduser(self, user):
        self.user.append(user)

    def neighbors_cci_calculation(self):
        self.cci = 0
        for ap in self.neighbor:
            if ap.channel == self.channel and ap != self:
                self.cci = self.cci + 1

    def association(self,):
        self.adduser()

    def check_state_change(self, t, timer, user, lowerbound):
        if timer == 0 or t%30 == 0 or len(user)< lowerbound: 
            return True

    def action():
        pass
    
    def update():
        pass

