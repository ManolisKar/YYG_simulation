# Epidemiological SEIR simulation, based on the YYG code

We used the publicly available SEIR model simulator from the YYG / [covid19-projections.com](https://covid19-projections.com) model. The very talented student I mentored for the ACT-SO competition used that as a tool to study the effect of medical technologies on pandemic outcomes.


## Introduction

The publicly available YYG SEIR simulator is used to simulate infections, hospitalizations, and deaths given a single set of parameters. It is a tool meant for simulations, not projections, as opposed to the full YYG model of [covid19-projections.com](https://covid19-projections.com) which has a ML layer to learn the parameters.

The SEIR model tracks probabilities of transition between the 4 states: **S**usceptible-**E**xposed-**I**nfectious-**R**ecovered/deceased. For more details on the YYG SEIR model see [their website](https://covid19-projections.com/model-details/).


<p align = "center">
<img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/SEIR.PNG" alt="Trulli" style="width:50%">
</p>
<p align = "center">
<sup>
Fig. 1: SEIR model diagram. 
</sup>
</p>


This is a fantastic and very useful tool for our study. It is simple to run, easily modifiable, and comes with "best" sets of parameters for each geographic region. 
Normally the simulation can be used to study hypothetical scenarios such as, "what would be the effect of initiating lockdowns a week earlier/later in the amount of hospitalizations and deaths?". My student instead used the simulation parameters to study the effect of novel medical technologies she is interested in, such as wider application of telehealth. 


As a baseline test of the out-of-the-box simulation performance, we plot U.S. deaths in the COVID-19 pandemic for the first ~9 months of the pandemic, and we compare its simulated predictions to the actual counts as found from an independent source. 
The simulation seems to be doing a very good job of simulating pandemic outcomes as experienced in the first year of the outbreak.


<p align = "center">
<img src="https://github.com/ManolisKar/YYG_simulation/blob/master/images/baseline_sim.png?raw=true" alt="Trulli" style="width:80%">
</p>
<p align = "center">
<sup>
Fig. 2: Baseline simulation matches reality well in terms of pandemic deaths.  
</sup>
</p>


## Parameters

There are several parameters that we need to provide the simulator before it can run. We describe the most important ones below.

*Note: All reproduction number parameters are the R values before population immunity is applied. For example, if the `REOPEN_R` in New York is 1.2 and 20% of the population is infected. then the "true" Rt is 1.2 * 0.8 = 0.96.*

#### `INITIAL_R_0`

This is the initial basic reproduction number (R_0). This value is usually between 0.8-6. Read more about our R_t estimates [here](https://covid19-projections.com/about/#effective-reproduction-number-r).

#### `LOCKDOWN_R_0`

This is the post-mitigation effective reproduction number (R_t). This value is usually between 0.3-1.5.

#### `INFLECTION_DAY`

This is the date of the inflection point when `INITIAL_R_0` transitions to `LOCKDOWN_R_0`. This is usually an indicator of when people in a region began social distancing. For example, in New York, the inflection day is around [March 14](https://twitter.com/youyanggu/status/1262881629376180227).

#### `RATE_OF_INFLECTION`

This is the rate at which the `INITIAL_R_0` transitions to `LOCKDOWN_R_0`. A number closer to 1 indicates a faster transition (i.e. faster lockdown), while a number closer to 0 indicates a slower transition. For most region, this value is between 0.15-0.5. The more localized a region, the higher the rate of inflection. So for example, we estimate New York City has a `RATE_OF_INFLECTION` between 0.4-0.5, while the US as an entire country has a `RATE_OF_INFLECTION` of approximately 0.2-0.3.

#### `MORTALITY_RATE`

This is the initial estimate of the infection fatality rate (IFR). This value is usually between 0.005-0.0125. Read more about our IFR estimates [here](https://covid19-projections.com/about/#infection-fatality-rate-ifr).



## Parameter scans

We iterate the simulation over many trials, modifying the value of four main parameters to characterize their effect on pandemic deaths. 
We also define two simulated scenarios, other than the baseline: one where advanced medical technologies were available, and used to ameliorate the effects of the pandemic; and one where the disease parameters were just slightly worse than they happened to be for COVID-19, averaged over the U.S.


<p align = "center">
<img src="https://github.com/ManolisKar/YYG_simulation/blob/master/images/parameter_scans.png?raw=true" alt="Trulli" style="width:90%">
</p>
<p align = "center">
<sup>
Fig. 3: Parameter scans to characterize their effect on pandemic deaths. Three parameter values denote different scenarios: baseline/reality (blue), a scenario where advanced technologies are available (green), and one where the disease parameters are slightly worse than they were for COVID-19 (red).
</sup>
</p>


Then we modify all 4 parameters at the same time, to better understand their combined effect. In Fig. 4 we plot the hyper-surface of maximum deaths in the sub-space of two of the modified parameters. Of course the validity of simulation is limited when we extrapolate to the region of tens of millions of deaths within the first pandemic year.

<p align = "center">
<img src="https://github.com/ManolisKar/YYG_simulation/blob/master/images/amias_3D-INITIAL_R_0_MORTALITY_RATE.png?raw=true" alt="Trulli" style="width:90%">
</p>
<p align = "center">
<sup>
Fig. 4: Pandemic deaths (in the vertical axis, in 1e7 units) versus the Initial R_0 and the Mortality Rate parameters - though all four parameters are being modified. The surface of maximum deaths is plotted for each parameter combination. 
</sup>
</p>


Finally we set the four examined parameters to their values under the three scenarios identified in Fig. 3. 
The comparative pandemic outcomes in deaths per day are plotted in Fig. 5 below. 
We see that very modest changes in pandemic parameters can have a massive impact on outcomes. The modeled use of advanced technologies could squash pandemic deaths down at the ~3% level. 

On the other hand, very slight increase in disease parameters (a scenario of a slightly more dangerous and lethal disease than COVID-19, keeping the parameters realistic as compared to other diseases and past pandemics) could result in ~300% more dead. 
In fact this latter estimate is moderated by the immunity effect, which vasly suppresses deaths after a large fraction of the population thas been infected. But the extrapolation of the simulated immunity effect in a region far outside where it was modeled cannot be trusted. 

<p align = "center">
<img src="https://github.com/ManolisKar/YYG_simulation/blob/master/images/deaths_scenarios.png?raw=true" alt="Trulli" style="width:90%">
</p>
<p align = "center">
<sup>
Fig. 5: Pandemic deaths per day under the three scenarios identified in Fig. 3. Also noted in the legend are the total deaths in the first 9 months for each scenario.
</sup>
</p>
