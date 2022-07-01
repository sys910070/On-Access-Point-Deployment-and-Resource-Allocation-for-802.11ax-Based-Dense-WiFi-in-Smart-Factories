import numpy as np
import matplotlib.pyplot as plt
import os

fairness_dap = np.load('DAP/data/fairness_record.npy')
total_throughput_record_dap = np.load('DAP/data/total_throughput_record.npy')
lost_device_dap = np.load('DAP/data/lost_device.npy')
active_ap_dap = np.load('DAP/data/active_ap.npy')

fairness_random = np.load('random/data/fairness_record.npy')
total_throughput_record_random = np.load('random/data/total_throughput_record.npy')
lost_device_random = np.load('random/data/lost_device.npy')
active_ap_random = np.load('random/data/active_ap.npy')

def graph_fairness(t, fairness_dap, fairness_random):
    plt.figure(figsize=(16,12))
    plt.title('fairness')
    plt.xlabel('time')
    plt.ylabel('fairness')
    plt.plot(t, fairness_dap, '-o', label = 'DAP')
    plt.plot(t, fairness_random, '-o', label = 'random')
    plt.legend()
    plt.savefig('fig/fairness_with_no_obstacle')
    # plt.show()

def graph_total_throughput_record_dap(t, total_throughput_record_dap, total_throughput_record_random):
    plt.figure(figsize=(16,12))
    plt.title('total throughput record dap')
    plt.xlabel('time')
    plt.ylabel('total throughput record dap')
    plt.plot(t, total_throughput_record_dap, '-o', label = 'DAP')
    plt.plot(t, total_throughput_record_random, '-o', label = 'random')
    plt.legend()
    plt.savefig('fig/total_throughput_record_dap number with no obstacle')
    # plt.show()

def graph_lost_device(t, lost_device_dap, lost_device_random):
    plt.figure(figsize=(16,12))
    plt.title('lost device')
    plt.xlabel('time')
    plt.ylabel('lost device')
    plt.plot(t, lost_device_dap, '-o', label = 'DAP')
    plt.plot(t, lost_device_random, '-o', label = 'random')
    plt.legend()
    plt.savefig('fig/lost_device_with_no_obstacle')
    # plt.show()

def graph_active_ap(t, active_ap_dap, active_ap_random):
    plt.figure(figsize=(16,12))
    plt.title('active ap')
    plt.xlabel('time')
    plt.ylabel('active ap')
    plt.plot(t, active_ap_dap, '-o', label = 'DAP')
    plt.plot(t, active_ap_random, '-o', label = 'random')
    plt.legend()
    plt.savefig('fig/active_ap_with_no_obstacle')
    # plt.show()

if not os.path.exists('fig'):
    os.mkdir('fig')
t = np.arange(len(fairness_dap))
graph_fairness(t, fairness_dap, fairness_random)
graph_total_throughput_record_dap(t, total_throughput_record_dap, total_throughput_record_random)
graph_lost_device(t, lost_device_dap, lost_device_random)
graph_active_ap(t, active_ap_dap, active_ap_random)