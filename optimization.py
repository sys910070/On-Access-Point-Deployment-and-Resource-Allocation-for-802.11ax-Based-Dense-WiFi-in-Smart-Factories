# this file is for each 30s update
from parameter import*
from utils import*

def mode1(ap_list, device_list):
    pass

def mode2(ap_list, device_list):
    pass


def power_adjust(ap_list):
    for ap in ap_list:
        if len(ap.user) != 0:
            for power in power_level:
                if range_decode(power) >= max_dis_device(ap):
                    ap.power_change(power, ap_list)
                    break
                
def channel_adjust(ap_list):
    # firstly sort the quene indecending order for the most users ap in the first position
    q = sorted(ap_list, key = lambda ap: len(ap.user), reverse = True)
    # try to increase channel bandwidth without increasing cci value
    for ap in q:
        if len(ap.user) == 0:
            break
        else:
            pre_cci = ap.cci
            ch_dic[ap.channel].reverse()
            for channel in ch_dic[ap.channel]:
                ap.channel = channel
                ap.cci_calculation()
                if ap.cci - pre_cci < 3:
                    break
            ch_dic[ap.channel].reverse()
            
def bandwidth_decrease(ap):
    pass