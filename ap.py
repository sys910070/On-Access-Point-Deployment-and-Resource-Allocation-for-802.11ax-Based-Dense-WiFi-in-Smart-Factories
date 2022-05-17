class ap:
    def __init__(self, x, y, power, channel, capacity, id, type_ap):
        self.x = x
        self.y = y
        self.power = power
        self.channel = channel
        self.capacity = capacity
        self.id = id
        self.type = type_ap
    
    def check_state(self, d_num):
        if d_num == 0:
            state = IDLE

    def st