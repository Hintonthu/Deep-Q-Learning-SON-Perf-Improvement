#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:38:03 2018

@author: farismismar
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import scipy.special
import matplotlib.ticker as tick

import os
os.chdir('/Users/farismismar/Desktop/E_Projects/UT Austin Ph.D. EE/Papers/Conferences to ASILOMAR/testbed')

qfunc = lambda x: 0.5-0.5*scipy.special.erf(x/np.sqrt(2))

# This has the Delta_gamma component
def ber_modified(sinr, delta=0, q=140):
    # sinr is in dB
    error = 1 - (1 - qfunc(np.sqrt(2.*(delta + 10**(sinr/10.))))) ** q # ** q
    return error


sinr = np.linspace(0,18,100)
#per = [ber(x) for x in sinr]

#plt.figure(figsize=(7,5))
#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')
##plot_edge, = plt.semilogy(sinr, ber_modified(sinr, delta=0, q=1), linestyle='-', color='k', label='QPSK (one OFDM symbol)')
#
#ax = plt.gca()
#ax.set_yscale('log')
#ax.get_xaxis().get_major_formatter().labelOnlyBase = False
#
#plot_baseline, = plt.semilogy(sinr, ber_modified(2.*sinr), linestyle='-', color='b', label='Average user $i$ (FPA)')
#
## Note the improvement was computed from Fig 11 in the paper.
##plot_vpc, = plt.semilogy(sinr, ber_modified(2.*sinr, 2/20+3*18/20), linestyle='-', color='r', label='Average user $i$ (Vanilla power control)')
#plot_dpc, = plt.semilogy(sinr, ber_modified(2.*sinr, 3*18/20), linestyle='-', color='g', label='Average user $i$ (DQN)')
#
#plt.grid(True,which="both")#,ls="-", color='0.65')
#
#plt.xlabel('Average DL SINR (dB)')
#plt.xlim(xmin=0,xmax=9)
#plt.ylabel('$\Xi$ PER')
#plt.title('Voice Packet Error Lower Bound Plot vs SINR -- One VoLTE Frame')
#
#plt.legend(handles=[plot_baseline, plot_dpc]) #plot_vpc, plot_dpc])
#plt.savefig('figures/packet_error.pdf', format="pdf")
#plt.show()
#plt.close()


tau = 20
#vanilla_tpc = ['start', 0, 'network', 2, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'end']
#vanilla_tpc = vanilla_tpc[1::2]
#vanilla_tpc.insert(0, 0) # initial state


deepq_tpc = ['start', 0, 'network', 2, 'network', 3, 'network', 3, 'network', 0, 'network', 0, 'network', 3, 'network', 3, 'network', 4, 'network', 0, 'network', 3, 'network', 2, 'network', 0, 'network', 3, 'network', 3, 'network', 0, 'ABORTED']
#deepq_tpc = ['start', 0, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'end'] # TPC 111

deepq_tpc = deepq_tpc[1::2]
deepq_tpc.insert(0, 0)
deepq_tpc = np.array(deepq_tpc)
'''
Q-learning
Episode 1018 finished after 19 timesteps (and epsilon = 0.01).
Action progress: 

SINR progress: 
['start', 4.0, 3.0, 4.0, 2.0, 0.0, 1.0, 2.0, 3.0, 4.0, 2.0, 3.0, 1.0, 2.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 'end']

Deep Q-Learning
Episode 1018 finished after 17 timesteps (and epsilon = 0.01).
Action progress: 
['start', 0, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'network', 3, 'end']
SINR progress: 
['start', 4.0, 2.0, 3.0, 4.0, 5.0, 3.0, 1.0, 2.0, 0.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 'end']
'''

# Convert actions to actual SINR changes
deepq_tpc[deepq_tpc == 0] = 0
deepq_tpc[deepq_tpc == 1] = -3
deepq_tpc[deepq_tpc == 2] = -1
deepq_tpc[deepq_tpc == 3] = 1
deepq_tpc[deepq_tpc == 4] = 3

time= np.arange(tau)

fig, ax1 = plt.subplots(figsize=(7,5))
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.grid(True)
fpa = ax1.axhline(y=0, xmin=0, color="green", linewidth=1.5, label='Power commands -- FPA')
#vanilla, = ax1.step(np.arange(len(vanilla_tpc)), vanilla_tpc, color='b', linewidth=2.5, label='TPC -- Vanilla')#
deep, = ax1.step(np.arange(len(deepq_tpc)), deepq_tpc, color='b', label='Power commands -- DQN')#
ax1.set_xlabel('Transmit time interval (TTI)')
ax1.set_ylabel('Number of power commands')
ax1.set_yticks([-1,0,1,2,3])
ax1.xaxis.set_major_formatter(tick.FormatStrFormatter('%0g'))
ax1.xaxis.set_ticks(np.arange(0, tau + 1))
#ax2 = ax1.twinx()
#sinr, = plt.plot(time, SINR, linestyle='-', color='b', label='DL SINR')
plt.title(r'Episode $\tau = 111$ -- Power Commands ')
plt.legend(handles=[fpa, deep])# vanilla, deep])
#ax2.set_ylabel('Average DL SINR $\gamma_{DL}$(dB)')

plt.xlim(xmin=0,xmax=tau)

fig.tight_layout()
plt.savefig('figures/tpc.pdf', format="pdf")
plt.show(fig)
plt.close(fig)



#
## Compute retainability
#for time in [ 30e3, 60e3]:
#    for ret in [0.3448, .7082, .8389]:
#        tau = 20
#        N = np.ceil(time/tau)
#        print('{}, {:.2f}%, {:.2f}%'.format(time, 100 * ret, 100 * ret ** N))
#    


# Plot MOS
tau = 20 # ms
T = tau #6 * 1e3 * tau # 120 sec

sinr = np.linspace(-2,14,100)

#def scale(per):  
    #per_scaled = [0.005 if i < -2 else (0.5 * (-2 - i) / (-2 - max(per))) for i in per]
#    per_scaled = [0.005 + i for i in per_scaled] # 0.05% is the minimum value
    
 #   return per_scaled



# TODO:
 # Obtain the corrective/improvement factors from the PC plot
def payload(T, tau=20, NAF=0.5, Lamr=0, Lsid=61): # T and tau in ms, Lamr/Lsid is in bits
    Lsid = Lsid * tau / 8  # from bits to bytes per sec
    return NAF * Lamr * np.ceil(T/tau) + (1 - NAF) * Lsid * np.ceil(T/(8*tau))

fig = plt.figure(figsize=(7,5))
for improvement in np.array([0, -1 * 2/20 +1 * 17/20 ]):#2/20+3*18/20,3*18/20]): 
    result = []
    
    for framelength in np.arange(1000): # 1000 taus
        volterate = 23.85 # kbps
        NAF = 0.7
        
        # something is wrong here with ber..
        ber = [ber_modified(x, delta=improvement, q=7*framelength*tau) for x in sinr]
        per = np.round(np.log10(ber), 0) # we actually need the exponent.
        N = len(per)
        fer = sum([1 for x in per if x > -2]) / N #scale(per)  # will get a frame error for this bit error rate
        Lamr = volterate * tau / 8 # in bytes per sec
        payld = payload(T=tau, tau=tau, NAF=NAF, Lamr=Lamr) # in bytes
        MOS = 4 - 0.7*np.log(fer) - 0.1 * np.log(tau * framelength * fer * N) # fer ok, second term: duration of lost packets in ms?

        MOS = min(4, MOS) #4 if MOS >= 4 else MOS # for i in MOS]
        MOS = max(1, MOS) #1 if MOS <= 1 else MOS# for i in MOS]
    #    print(improvement, fer, MOS)
        result.append(MOS)
    
        #print('{} {:.0f}% {:.1f}'.format(volterate, 100 * NAF, payld))
        if (improvement == 0):
            str = 'FPA'
        elif (improvement == -1 * 2/20 +1 * 17/20):
            str = 'Closed-loop'
    plt.plot(result, label='AMR = {} kbps, AF = {}, Power control = {}'.format(volterate, NAF, str))
    
    
plt.legend()
plt.title('Experimental mean opinion score vs packet error rate')
plt.xlabel('Packet error rate')
plt.ylabel('MOS')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.xlim(xmin=0,xmax=250)

plt.grid(True)

# Fix the x axis to show packet error rates 
ax = plt.gca()
#ax.set_xticks([0,200,400,600,800,1000])
ax.set_xticks([0,50,100,150,200,250])
#ax.set_xticklabels([0,0.1,0.2,0.3,0.4,0.5])
ax.set_xticklabels([0,0.05,0.10,0.15,0.2,0.25])


plt.savefig('figures/mos.pdf', format='pdf')
plt.show()
plt.close(fig)




####################################
# Plotting the episodes on one graph
####################################
SINR_MIN = -3 #dB  
baseline_SINR_dB = 4.0
final_SINR_dB = baseline_SINR_dB + 2.0 # this is the improvement
max_timesteps_per_episode = 20
max_episodes_to_run = 725

episode_index = 724 #379 #825


#score_progress_fpa = [4.0,4.0,4.0,4.0,4.0,4.0,4.0,1.0,1.0,1.0,-3,-3.0,-3.0,-3,-3,-3,-3,-0.0,-0.0,-0.0,5.0]
#score_progress_cl = [4.0,3.0,4.0,0.0,1.0,-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0,4.0,0.0,1.0,-1.0,0.0,4.0,5.0,6.0]
score_progress_cl = [4.0,3.0,4.0,5.0,1.0,-1.0,-3.0,-2.0,-1.0,-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0,3.0,1.0,6.0]
score_progress_fpa = [4.0,4.0,2.0,-3,-3.0,-3.0,-3.0,-3.0,-3,-3,-3,-3.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,-0.0,-0.0]
#

# Do some nice plotting here
fig = plt.figure()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.xlabel('Transmit Time Intervals (1 ms)')

# Only integers                                
ax = fig.gca()
ax.xaxis.set_major_formatter(tick.FormatStrFormatter('%0g'))
ax.xaxis.set_ticks(np.arange(0, max_timesteps_per_episode + 1))

ax.set_autoscaley_on(False)

plt.plot(score_progress_fpa, marker='o', linestyle=':', color='b', label='FPA')
plt.plot(score_progress_cl, marker='D', linestyle='-', color='k', label='CL')

plt.xlim(xmin=0, xmax=max_timesteps_per_episode)

plt.axhline(y=SINR_MIN, xmin=0, color="red", linewidth=1.5)
plt.axhline(y=final_SINR_dB, xmin=0, color="green",  linewidth=1.5)
plt.ylabel('Average DL Received SINR (dB)')
plt.title('Episode {0} / {1}'.format(episode_index + 1, max_episodes_to_run))
plt.grid(True)
plt.ylim(-8,10)
plt.legend()

plt.savefig('figures/episode_{}_output.pdf'.format(episode_index + 1), format="pdf")
plt.show(block=True)
plt.close(fig)

