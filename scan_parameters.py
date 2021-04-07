'''
Scan individual parameters in the YYG/C19Pro SEIR model.
Output plots with dependence of total deaths to these parameters.

Sample usage: `python scan_parameters.py

'''

import run_simulation

import numpy as np
import argparse
import sys

import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.titlesize': 14})
plt.rcParams.update({'axes.labelsize': 10})
plt.rcParams.update({'lines.linewidth' : 2})
plt.rcParams.update({'lines.markersize' : 12})
plt.rcParams.update({'xtick.labelsize' : 13})
plt.rcParams.update({'ytick.labelsize' : 13})



## args needed to run the simulation main
main_args = argparse.Namespace(
    best_params_dir='best_params/latest', best_params_type='mean',
    change_param=None, country='US', quarantine_effectiveness=-1,
    quarantine_perc=0, region='', save_csv_fname='', set_param=None,
    simulation_end_date=None, simulation_start_date=None,
    skip_hospitalizations=False, subregion='', verbose=False
)


###
### Define range of parameters
###

params=['INITIAL_R_0',
        'MORTALITY_RATE',
        'LOCKDOWN_R_0',
        'RATE_OF_INFLECTION'
        ]

par_range={}
par_range['INITIAL_R_0'] = np.arange(0.6,6.,0.2)
par_range['MORTALITY_RATE'] = np.arange(0.005,0.05,0.005)
par_range['LOCKDOWN_R_0']=np.arange(0.5,1.5,0.1)
par_range['RATE_OF_INFLECTION']=np.arange(0.15, 0.7, 0.1)

## baseline parameters
default={}
default['INITIAL_R_0'] = 2.2637755302375644
default['MORTALITY_RATE'] = 0.01
default['LOCKDOWN_R_0']=0.9038440070216232
default['RATE_OF_INFLECTION']=0.35245146707754205
default['REOPEN_R']=1.2681889965435804
default['POST_REOPEN_EQUILIBRIUM_R']=1.0073471671122585

## best-case parameters
best={}
best['INITIAL_R_0'] = 1.8
best['MORTALITY_RATE'] = 0.007
best['LOCKDOWN_R_0']=0.7
best['RATE_OF_INFLECTION']=0.5

## worst-case parameters
worst={}
worst['INITIAL_R_0'] = 4.
worst['MORTALITY_RATE'] = 0.03
worst['LOCKDOWN_R_0']=1.2
worst['RATE_OF_INFLECTION']=0.25

set_params=[]
for param in params:
    set_params += [(param, default[param])]
main_args.set_param = set_params
default['total_deaths'] = run_simulation.main(main_args)


fig,axs=plt.subplots(2,2)
for i,param in enumerate(params):
    ## Scan each parameter
    if i<2:
        row,col=0,i
    else:
        row,col=1,i-2

    x,y=[],[]
    for value in par_range[param]:
        x+=[value]
        main_args.set_param=[(param, value)]
        y+=[ run_simulation.main(main_args) ]
    axs[row,col].plot(x,y, label='%s scan'%param)
    axs[row,col].scatter(default[param], default['total_deaths'], color='blue', label='baseline simulation')
    main_args.set_param=[(param, best[param])]
    best['total_deaths'] = run_simulation.main(main_args)
    main_args.set_param=[(param, worst[param])]
    worst['total_deaths'] = run_simulation.main(main_args)
    axs[row,col].scatter(best[param], best['total_deaths'], color='g', label='best-case scenario')
    axs[row,col].scatter(worst[param], worst['total_deaths'], color='r', label='worst-case scenario')
    axs[row,col].set_title(param)
    axs[row,col].set_xlabel(param)
    axs[row,col].set_ylabel('Total deaths')
    axs[row,col].legend()
    main_args.set_param=[(param, default[param])]

plt.tight_layout()
plt.show()

#sys.exit()

