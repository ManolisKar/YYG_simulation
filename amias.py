#!/usr/bin/env python

import os,sys
import pickle
import math
import random
import numpy as np

from mpl_toolkits import mplot3d
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.titlesize': 25})
plt.rcParams.update({'axes.labelsize': 23})
plt.rcParams.update({'lines.linewidth' : 3})
plt.rcParams.update({'lines.markersize' : 20})
plt.rcParams.update({'xtick.labelsize' : 20})
plt.rcParams.update({'ytick.labelsize' : 20})
import seaborn as sns

import readline,rlcompleter
readline.parse_and_bind('tab:complete')

__doc__ = '''
Plot total deaths versus sampled simulation model parameters.
'''

import argparse
parser = argparse.ArgumentParser(description=__doc__, epilog=' ', formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--nbins',type=int,default=10,help='Number of bins for each parameter')
#parser.add_argument('--chi2-cutoff',type=float,default=0,help='Cut trials that result in chi2 higher than this cutoff')
parser.add_argument('infiles', type=str, nargs='+', help='AMIAS files to be processed -- for now expected to be pkl files with dict of parameter grid')
args = parser.parse_args()

infiles = args.infiles
n_files = len(infiles)
nbins=args.nbins

## Data-holding structure
data={}


### Iterate over all input files, reading for all fit-types
## (for now only expecting single file)
for i_file,infile_name in enumerate(infiles):
    print( 'Reading in file #%d : \n %s' % (i_file,infile_name) )
    infile = open(infile_name,'rb')
    data = pickle.load(infile)

print( 'Smallest number of deaths found: ', np.min(data['total_deaths'] ) )
print( 'Largest number of deaths found: ', np.max(data['total_deaths'] ) )


## Purge any parameters that were kept constant
for param in (x for x in data.keys() if np.std(data[x])==0):
    print( param )
    del data[fit_type][param]


#### 
#### Plotting
#### 


## function to make bins out of an array
def binnies(data_array,n_bins=nbins):
    nparray = np.array(data_array)
    binwidth=(max(nparray)-min(nparray))/n_bins
    bins=np.linspace(min(nparray), max(nparray), n_bins) + binwidth/2
    return bins,binwidth

## pass 1D arrays, make 2D arrays mesh and corresponding min/max of the z-variable per 2D bin
## eg min chi2 per bin, or max deaths per bin       
def make_2D_arrays(x_array,y_array,z_array, minmax='max'): 
    x=np.array(x_array)
    y=np.array(y_array)
    z=np.array(z_array)
    x_bins,x_binwidth=binnies(x_array)
    y_bins,y_binwidth=binnies(y_array)
    X_bins, Y_bins = np.meshgrid(x_bins, y_bins)
    Z_bins = np.zeros_like(X_bins)
    for i in range(len(X_bins)):
       for j in range(len(X_bins[i])):
           bin_z = z[ (abs(x-X_bins[i][j])<x_binwidth) & (abs(y-Y_bins[i][j])<y_binwidth) ]
           if bin_z.any():
               if 'max' in minmax: Z_bins[i][j] =  max( bin_z )
               if 'min' in minmax: Z_bins[i][j] =  min( bin_z )
    return X_bins,Y_bins,Z_bins

## function to save figure
def save_plot(fig,param_name,stem='amias',filetype='png'):
    outfile_basename = '%s-%s'%(stem,param_name)
    print( 'writing out %s.%s...'%(outfile_basename,filetype) )
    fig.savefig(outfile_basename+'.'+filetype, bbox_inches='tight')
    #print( 'writing out %s.pkl...'%outfile_basename )
    #pickle.dump(fig,open(outfile_basename+'.pkl','wb'))

## functions to plot 3D with triangulation surfaces 
def plot3D_trisurf(x,y,z,title='plot',paramnames=['x','y','z']):
    plot = plt.figure(figsize=(12,9)).add_subplot(1,1,1,projection='3d',
        title=title
    )
    plot.plot_trisurf(x, y, z, cmap='hsv')
    ##plot.figure.colorbar(**something with axes here**, shrink=0.5, aspect=5)
    #plot.canvas.start_event_loop(sys.float_info.min) #workaround for Exception in Tkinter callback
    plt.show(block=False)
    save_plot(plot.figure,param_name='%s_%s' % (paramnames[0],paramnames[1]),
        stem='amias_3D',filetype='png')
def plot3D_surface(x,y,z,title='plot',paramnames=['x','y','z']):
    plot = plt.figure(figsize=(12,9)).add_subplot(1,1,1,projection='3d',
        title=title
    )
    plot.plot_surface(x, y, z, cmap='hsv')
    plot.set_xlabel('\n'+paramnames[0], linespacing=3.2)
    plot.set_ylabel('\n'+paramnames[1], linespacing=3.2)
    plot.set_zlabel('\n'+paramnames[2], linespacing=3.2)
    plot.dist = 10
    ##plot.figure.colorbar(**something with axes here**, shrink=0.5, aspect=5)
    #plot.figure.show()
    plt.show(block=False)
    #save_plot(plot.figure,param_name='%s_%s' % (paramnames[0],paramnames[1]),
    #   stem='amias_3D',filetype='png')

## function to bin and plot 3D surface vs the z-variable
def plot3D_vsZ(xvar,yvar,zvar='chi2',minmax='max'):
    X_bins,Y_bins,Z_bins = make_2D_arrays(data[xvar],data[yvar],data[zvar],minmax)
    if Z_bins.all():
        plot3D_surface(
            x=X_bins,
            y=Y_bins,
            z=Z_bins,
            title=r'%s vs %s' % (xvar,yvar),
            paramnames=[xvar,yvar,zvar]
        )
    else: 
        ## empty Chi2 bin; plot with different technique instead
        plot3D_trisurf(
            x=X_bins[np.where(Z_bins>0)],
            y=Y_bins[np.where(Z_bins>0)],
            z=Z_bins[np.where(Z_bins>0)],
            title=r'%s vs %s' % (xvar,yvar),
            paramnames=[xvar,yvar,zvar]
        )


## Plotting commands for parameter combinations in passed data
plot3D_vsZ('INITIAL_R_0','MORTALITY_RATE','total_deaths',minmax='max')

'''
if 'IFR' in data.keys():
    plot3D_vsZ(
'''

sys.exit(0)


### Extract correlations and plot parameter histograms.
### For that need to select a chi2 cutoff:
### Without a cutoff then all vars are uniformly distributed and correlations don't make sense.
cutoff={}
for fit_type in data.keys():
    if args.chi2_cutoff:
        cutoff[fit_type] = args.chi2_cutoff
    else:
        cutoff[fit_type] = savedata[fit_type].reduced_chi_square + 1./savedata[fit_type].N_dof
    print( '\n Chi2 cutoff for %s is %f\n' % (fit_type, cutoff[fit_type]) )

## Put all data in a pandas dataframe, much easier to handle correlations
import pandas as pd
npdata={}
df={}
for fit_type in data.keys():
    npdata[fit_type]=np.array(data[fit_type][data[fit_type].keys()[0]])[np.array(data[fit_type]['chi2'])<cutoff[fit_type]]
    labels=[data[fit_type].keys()[0]]
    for key in data[fit_type].keys()[1:]:
        npdata[fit_type]=np.vstack((npdata[fit_type],np.array(data[fit_type][key])[np.array(data[fit_type]['chi2'])<cutoff[fit_type]] ))
        labels.append(key)
    df[fit_type]=pd.DataFrame(data=npdata[fit_type],index=labels)
    df[fit_type]=df[fit_type].T ##transpose rows/columns
    corr = df[fit_type].corr()
    corr=corr.dropna(axis=0,how='all')
    corr=corr.dropna(axis=1,how='all')
    print( 'Correlation matrix:\n', corr )

    fig, ax = plt.subplots(figsize=(10, 6))
    hm = sns.heatmap(corr, ax=ax, cmap="coolwarm",fmt='.2f',linewidths=.05)
    fig.subplots_adjust(top=0.93)
    t= fig.suptitle('Correlation Heatmap, %s'%fit_type, fontsize=14)
    plt.show()
    save_plot(fig,fit_param_name='%s' % fit_type,
            stem='amias_heatmap',filetype='png')

    ## Jointplots
    data_pairs=[['r','phi_a'],['tau_cbo','A_cbo'],['K','N0']]
    for pair in data_pairs:
        if pair[0] in df[fit_type] and pair[1] in df[fit_type]:
            sns.jointplot(x=pair[0], y=pair[1], data=df[fit_type],kind='reg')
            plt.show()
