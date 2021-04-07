'''Script to iteratively run the simulations using the YYG/C19Pro SEIR model.

Sample usage: `python iterate_run_simulation.py -example_arg value

'''

import run_simulation

import numpy as np
import argparse

## args needed to run the simulation main
main_args = argparse.Namespace(
    best_params_dir='best_params/latest', best_params_type='mean',
    change_param=None, country='US', quarantine_effectiveness=-1,
    quarantine_perc=0, region='', save_csv_fname='', set_param=None,
    simulation_end_date=None, simulation_start_date=None,
    skip_hospitalizations=False, subregion='', verbose=False
)


###
### Define the grid of parameters
###
param_grid={}

# initial basic reproduction number (R_0)
R0_values=np.arange(0.6,6.,0.2)
default_R0=2.2637755302375644
default_REOPEN_R=1.2681889965435804
default_POST_REOPEN_EQUILIBRIUM_R=1.0073471671122585
# infection fatality rate
IFR_values=np.arange(0.005,0.05,0.003)## default is 0.01
# Lockdown R0, expressed as fraction of R0
LOCKDOWN_R_0_fraction_values=np.arange(0.005,0.6,0.05)## default is ~0.4
# rate of inflection, ie transition from R0 to LOCKDOWN_R0
RATE_OF_INFLECTION_values=np.arange(0.15, 0.99, 0.1)## default is 0.35245146707754205

param_grid['INITIAL_R_0']=[]
param_grid['MORTALITY_RATE']=[]
param_grid['LOCKDOWN_R_0']=[]
param_grid['RATE_OF_INFLECTION']=[]
param_grid['total_deaths']=[]

## Iterate over the simulation, to extract the number of deaths for each parameter set
for R0_value in R0_values:
    R0_scale=R0_value/ default_R0
    REOPEN_R_value=default_REOPEN_R*R0_scale
    POST_REOPEN_EQUILIBRIUM_R_value=default_POST_REOPEN_EQUILIBRIUM_R*R0_scale
    ## no need to apply the scale to LOCKDOWN_R0, as we are scaling it separately
    for IFR_value in IFR_values:
        for RATE_OF_INFLECTION_value in RATE_OF_INFLECTION_values:
            for LOCKDOWN_R_0_fraction_value in LOCKDOWN_R_0_fraction_values:
                LOCKDOWN_R_0_value = LOCKDOWN_R_0_fraction_value*R0_value
                main_args.set_param=[('INITIAL_R_0', R0_value),
                                     ('MORTALITY_RATE', IFR_value),
                                     ('RATE_OF_INFLECTION', RATE_OF_INFLECTION_value),
                                     ('LOCKDOWN_R_0', LOCKDOWN_R_0_value)]
                param_grid['INITIAL_R_0'] += [R0_value]
                param_grid['MORTALITY_RATE'] += [IFR_value]
                param_grid['RATE_OF_INFLECTION'] += [RATE_OF_INFLECTION_value]
                param_grid['LOCKDOWN_R_0'] += [LOCKDOWN_R_0_value]
                param_grid['total_deaths'] += [run_simulation.main(main_args)]

        
import pickle 
outfile=open('param_grid.pkl','wb')
pickle.dump(param_grid,outfile)
outfile.close()
