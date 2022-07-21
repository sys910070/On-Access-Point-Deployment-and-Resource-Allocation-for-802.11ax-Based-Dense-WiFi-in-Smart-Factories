import numpy as np
import matplotlib.pyplot as plt
import os

environment = ['no_obstacle', 'symmetric_obstacle', 'asymmetric_obstacle']
def graph_fairness(t, fairness_dap, fairness_random, fairness_sequential):
    plt.figure(figsize=(16,12))
    plt.title('fairness')
    plt.xlabel('time')
    plt.ylabel('fairness')
    plt.plot(t, fairness_dap, '-o', label = 'DAP')
    plt.plot(t, fairness_random, '-o', label = 'random')
    plt.plot(t, fairness_sequential, '-o', label = 'sequential')
    plt.xlim(0, len(total_throughput_record_dap)+1)
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig(f'fig/{factory_environment}/fairness')
    # plt.show()

def graph_total_throughput(t, total_throughput_record_dap, total_throughput_record_random, total_throughput_record_sequential):
    plt.figure(figsize=(16,12))
    plt.title('total throughput')
    plt.xlabel('time')
    plt.ylabel('total throughput')
    plt.plot(t, total_throughput_record_dap, '-o', label = 'DAP')
    plt.plot(t, total_throughput_record_random, '-o', label = 'random')
    plt.plot(t, total_throughput_record_sequential, '-o', label = 'sequential')
    plt.xlim(0, len(total_throughput_record_dap)+1)
    plt.ylim(0, 8000)
    plt.legend()
    plt.savefig(f'fig/{factory_environment}/total_throughput')
    # plt.show()

def graph_lost_device(t, lost_device_dap, lost_device_random, lost_device_sequential):
    plt.figure(figsize=(16,12))
    plt.title('lost device')
    plt.xlabel('time')
    plt.ylabel('lost device')
    plt.plot(t, lost_device_dap, '-o', label = 'DAP')
    plt.plot(t, lost_device_random, '-o', label = 'random')
    plt.plot(t, lost_device_sequential, '-o', label = 'sequential')
    plt.xlim(0, len(total_throughput_record_dap)+1)
    plt.ylim(0, 100)
    plt.legend()
    plt.savefig(f'fig/{factory_environment}/lost_device')
    # plt.show()

def graph_active_ap(t, active_ap_dap, active_ap_random, active_ap_sequential):
    plt.figure(figsize=(16,12))
    plt.title('active ap')
    plt.xlabel('time')
    plt.ylabel('active ap')
    plt.plot(t, active_ap_dap, '-o', label = 'DAP')
    plt.plot(t, active_ap_random, '-o', label = 'random')
    plt.plot(t, active_ap_sequential, '-o', label = 'sequential')
    plt.xlim(0, len(total_throughput_record_dap)+1)
    plt.ylim(0, 81)
    plt.legend()
    plt.savefig(f'fig/{factory_environment}/active_ap')
    # plt.show()

for factory_environment in environment:
    fairness_dap = np.load(f'DAP/data/fairness_{factory_environment}.npy')
    total_throughput_record_dap = np.load(f'DAP/data/total_throughput_{factory_environment}.npy')
    lost_device_dap = np.load(f'DAP/data/lost_device_{factory_environment}.npy')
    active_ap_dap = np.load(f'DAP/data/active_ap_{factory_environment}.npy')

    fairness_random = np.load(f'random/data/fairness_{factory_environment}.npy')
    total_throughput_record_random = np.load(f'random/data/total_throughput_{factory_environment}.npy')
    lost_device_random = np.load(f'random/data/lost_device_{factory_environment}.npy')
    active_ap_random = np.load(f'random/data/active_ap_{factory_environment}.npy')

    fairness_sequential = np.load(f'sequential/data/fairness_{factory_environment}.npy')
    total_throughput_record_sequential = np.load(f'sequential/data/total_throughput_{factory_environment}.npy')
    lost_device_sequential = np.load(f'sequential/data/lost_device_{factory_environment}.npy')
    active_ap_sequential = np.load(f'sequential/data/active_ap_{factory_environment}.npy')

    if not os.path.exists('fig'):
        os.mkdir('fig/')
    if not os.path.exists(f'fig/{factory_environment}'):
        os.mkdir(f'fig/{factory_environment}')
    t = np.arange(len(fairness_dap))
    graph_fairness(t, fairness_dap, fairness_random, fairness_sequential)
    graph_total_throughput(t, total_throughput_record_dap, total_throughput_record_random, total_throughput_record_sequential)
    graph_lost_device(t, lost_device_dap, lost_device_random, lost_device_sequential)
    graph_active_ap(t, active_ap_dap, active_ap_random, active_ap_sequential)