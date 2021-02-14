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
R0_values=np.arange(0.5,9.9,0.5)
# infection fatality rate
IFR_values=np.arange(0.005,0.2,0.005)

param_grid['INITIAL_R_0']=[]
param_grid['MORTALITY_RATE']=[]
param_grid['total_deaths']=[]

## Iterate over the simulation, to extract the number of deaths for each parameter set
for R0_value in R0_values:
    for IFR_value in IFR_values:
        main_args.set_param=[('INITIAL_R_0', R0_value), ('MORTALITY_RATE', IFR_value)]
        param_grid['INITIAL_R_0'] += [R0_value]
        param_grid['MORTALITY_RATE'] += [IFR_value]
        param_grid['total_deaths'] += [run_simulation.main(main_args)]

        
import pickle 
outfile=open('param_grid.pkl','wb')
pickle.dump(param_grid,outfile)
outfile.close()
