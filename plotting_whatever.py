import numpy as np
import matplotlib.pyplot as plt
import os

# environment = ['no_obstacle', 'symmetric_obstacle', 'asymmetric_obstacle', 'real_factory_layout']
# def graph_fairness(t, fairness_dap, fairness_random, fairness_sequential):
#     plt.figure(figsize=(16,12))
#     plt.title('fairness')
#     plt.xlabel('time')
#     plt.ylabel('fairness')
#     plt.plot(t, fairness_dap, '-o', label = 'DAP')
#     plt.plot(t, fairness_random, '-o', label = 'random')
#     plt.plot(t, fairness_sequential, '-o', label = 'sequential')

#     plt.xlim(100, 601)
#     # plt.xlim(0, len(total_throughput_record_dap)+1)
#     plt.ylim(0, 1)
#     plt.legend()
#     plt.savefig(f'fig/{factory_environment}/fairness')
#     # plt.show()

# def graph_total_throughput(t, total_throughput_record_dap, total_throughput_record_random, total_throughput_record_sequential):
#     plt.figure(figsize=(16,12))
#     plt.title('total throughput')
#     plt.xlabel('time')
#     plt.ylabel('total throughput')
#     plt.plot(t, total_throughput_record_dap, '-o', label = 'DAP')
#     plt.plot(t, total_throughput_record_random, '-o', label = 'random')
#     plt.plot(t, total_throughput_record_sequential, '-o', label = 'sequential')
#     plt.xlim(100, 601)
#     # plt.xlim(0, len(total_throughput_record_dap)+1)
#     plt.ylim(0, 8000)
#     plt.legend()
#     plt.savefig(f'fig/{factory_environment}/total_throughput')
#     # plt.show()

# def graph_lost_device(t, lost_device_dap, lost_device_random, lost_device_sequential):
#     plt.figure(figsize=(16,12))
#     plt.title('lost device')
#     plt.xlabel('time')
#     plt.ylabel('lost device')
#     plt.plot(t, lost_device_dap, '-o', label = 'DAP')
#     plt.plot(t, lost_device_random, '-o', label = 'random')
#     plt.plot(t, lost_device_sequential, '-o', label = 'sequential')
#     plt.xlim(100, 601)
#     # plt.xlim(0, len(total_throughput_record_dap)+1)
#     plt.ylim(0, 100)
#     plt.legend()
#     plt.savefig(f'fig/{factory_environment}/lost_device')
#     # plt.show()

# def graph_active_ap(t, active_ap_dap, active_ap_random, active_ap_sequential):
#     plt.figure(figsize=(16,12))
#     plt.title('active ap')
#     plt.xlabel('time')
#     plt.ylabel('active ap')
#     plt.plot(t, active_ap_dap, '-o', label = 'DAP')
#     plt.plot(t, active_ap_random, '-o', label = 'random')
#     plt.plot(t, active_ap_sequential, '-o', label = 'sequential')
#     plt.xlim(100, 601)
#     # plt.xlim(0, len(total_throughput_record_dap)+1)
#     plt.ylim(0, 81)
#     plt.legend()
#     plt.savefig(f'fig/{factory_environment}/active_ap')
#     # plt.show()

def loss_device_vs_timer():
    plt.figure(figsize=(16,12))
    plt.title('Loss device vs timer', fontsize = 30)
    plt.xlabel('timer', fontsize = 30)
    plt.ylabel('average loss device', fontsize = 30)
    plt.bar(['2', '4', '6', '8', '10'], [13.37, 16.27, 18.82, 26.27, 33.49], width = 0.5)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # plt.xlim(2, 10)
    # plt.xlim(0, len(total_throughput_record_dap)+1)
    plt.ylim(0, 40)
    plt.savefig(f'fig/Loss device vs timer')
loss_device_vs_timer()

# for factory_environment in environment:
#     fairness_dap = np.load(f'DAP/data/fairness_{factory_environment}.npy')
#     total_throughput_record_dap = np.load(f'DAP/data/total_throughput_{factory_environment}.npy')
#     lost_device_dap = np.load(f'DAP/data/lost_device_{factory_environment}.npy')
#     active_ap_dap = np.load(f'DAP/data/active_ap_{factory_environment}.npy')

#     fairness_random = np.load(f'random/data/fairness_{factory_environment}.npy')
#     total_throughput_record_random = np.load(f'random/data/total_throughput_{factory_environment}.npy')
#     lost_device_random = np.load(f'random/data/lost_device_{factory_environment}.npy')
#     active_ap_random = np.load(f'random/data/active_ap_{factory_environment}.npy')

#     fairness_sequential = np.load(f'sequential/data/fairness_{factory_environment}.npy')
#     total_throughput_record_sequential = np.load(f'sequential/data/total_throughput_{factory_environment}.npy')
#     lost_device_sequential = np.load(f'sequential/data/lost_device_{factory_environment}.npy')
#     active_ap_sequential = np.load(f'sequential/data/active_ap_{factory_environment}.npy')

#     if not os.path.exists('fig'):
#         os.mkdir('fig/')
#     if not os.path.exists(f'fig/{factory_environment}'):
#         os.mkdir(f'fig/{factory_environment}')
#     t = np.arange(len(fairness_dap))
#     graph_fairness(t[10:61]*10, fairness_dap[10:61], fairness_random[10:61], fairness_sequential[10:61])
#     graph_total_throughput(t[10:61]*10, total_throughput_record_dap[10:61], total_throughput_record_random[10:61], total_throughput_record_sequential[10:61])
#     graph_lost_device(t[10:61]*10, lost_device_dap[10:61], lost_device_random[10:61], lost_device_sequential[10:61])
#     graph_active_ap(t[10:61]*10, active_ap_dap[10:61], active_ap_random[10:61], active_ap_sequential[10:61])

