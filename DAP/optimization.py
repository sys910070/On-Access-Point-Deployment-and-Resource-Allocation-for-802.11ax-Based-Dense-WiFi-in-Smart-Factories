# this file is for each 30s update
from action import A_State, D_State
from parameter import*
from utils import*

# this function is for 30s update, channel would be amplify as large as possible
def channel_amplification(ap_list):
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

# in version1, we attemp to give away some user to other active ap for those with lower user_throughput
# then, adjust power_level
# finally, attemp to make half of ap(high user_throughput) use smaller bandwidth 
def fairness_adjust_version1(ap_list, device_list):
    # calculate idle_ap number
    idle_ap = 0
    for ap in ap_list:
        if ap.power == 0:
            idle_ap += 1

    # sort the quene in decending order in order to place the least users' throughput in the first position
    q = sorted(ap_list, key = lambda ap: ap.user_throughput, reverse = False)
    for i in range(len(q)):
        q[i].ranking = i
    # for those ap in higher priority means its user_throughput is lower
    # switch those low throughput user to other active ap if ranking of other active ap is lower than current ap
    for ap in q:
        if ap.ranking >= idle_ap and ap.ranking <= idle_ap+(ap_num-idle_ap)/2:
            for user in ap.user:
                selected_ap = find_other_active_ap(user, ap_list)
                if selected_ap != None and selected_ap.ranking < ap.ranking:
                    user.ap.user.remove(user)
                    device_connect(user, selected_ap)
    
    # change state if necessary and adjust power_level
    for ap in ap_list:
        if len(ap.user) == 0:
            ap.power_change(0, ap_list)
            ap.channel = 0
            ap.state = A_State.idle
            ap.timer = a_state_timer_idle
        elif len(ap.user) >= ap.lowerbound:
            ap.state = A_State.active
            ap.timer = float('inf')
        else:
            ap.state = A_State.underpopulated
            ap.timer = a_state_timer_underpopulate
        power_adjustment(ap, ap_list)

    # switch those high user_throughput ap's bandwidth into 20MHz
    for ap in q:
        if ap.channel != 0:
            if ap.ranking >= idle_ap and ap.ranking <= idle_ap+(ap_num-idle_ap)/2:
                selected_channel = ap.channel
                curr_cci = ap.cci
                if ch_id_to_bw[ap.channel] != 20:
                    for ch in ch_dic[ap.channel]:
                        if ch_id_to_bw[ch] == 20:
                            ap.channel = ch
                            ap.cci_calculation()
                            if ap.cci <= curr_cci:
                                curr_cci = ap.cci
                                selected_channel = ch
                ap.channel = selected_channel

    cci_cal(ap_list)  
    throughput_cal(ap_list, device_list)
    fairness_index = fairness_cal(ap_list)
    return fairness_index

# in this version, we attemp to pair up two ap in each interference rage and try do balance their user_throughput 
def fairness_adjust_version2(ap_list, device_list):
    # sort the quene in decending order in order to place the least users' throughput in the first position
    q = sorted(ap_list, key = lambda ap: ap.user_throughput, reverse = False)
    for i in range(len(q)):
        q[i].ranking = i
    # reset ap's partner
    for ap in ap_list:
        ap.partner = None

    for ap in q:
        temp_ranking = 0
        selected_partner = None
        if ap.power != 0 and ap.partner == None:
            for neighbor in ap.neighbor_decode:
                if (neighbor.partner == None) and (neighbor.ranking > temp_ranking):
                    temp_ranking = neighbor.ranking
                    selected_partner = neighbor
            if selected_partner != None:
                ap.partner = selected_partner
                selected_partner.partner = ap

    for ap in ap_list:
        if ap.partner != None:
            # rank is lower means its user_throughput is lower than its partner, the lower ap is trying to giveaway its user to its partner
            if ap.ranking < ap.partner.ranking:
                for user in ap.user:
                    if user.type == ap.partner.type and distance((user.x, user.y), (ap.partner.x, ap.partner.y)) < range_decode(p_max) and len(ap.partner.user) < ap.partner.upperbound:
                        ap.partner.power_change(p_max, ap_list)
                        ap.user.remove(user)
                        device_connect(user, ap.partner)
                        power_adjustment(ap, ap_list)
                        power_adjustment(ap.partner, ap_list)
    
    # reset state if necessary
    for ap in ap_list:
        if len(ap.user) == 0:
            ap.power_change(0, ap_list)
            ap.channel = 0
            ap.state = A_State.idle
            ap.timer = a_state_timer_idle
        elif len(ap.user) >= ap.lowerbound:
            ap.state = A_State.active
            ap.timer = float('inf')
        else:
            ap.state = A_State.underpopulated
            ap.timer = a_state_timer_underpopulate 

    cci_cal(ap_list)  
    throughput_cal(ap_list, device_list)
    fairness_index = fairness_cal(ap_list)
    return fairness_index
