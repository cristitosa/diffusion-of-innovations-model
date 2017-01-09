# -*- coding: utf-8 -*-

"""
Run a complete analysis for a give parameter
"""

# Reset the kernel
get_ipython().magic('reset -f')      # analysis:ignore

import glob
import json
import os
import os.path as osp

from ipyparallel import Client

from algorithm import compute_run, generate_parameters
from plots import multiplot_adopters_and_global_utility
from utils import LOCATION, compute_global_utility_activation_value


#==============================================================================
# Simulation parameters and values
#==============================================================================
main_parameter = 'social_influence'
parameter_values = [0.1, 0.5, 0.7, 0.9]
number_of_times = 50
max_time = 60

# Parameters
parameters = dict(
    randomness = 0.01,
    number_of_neighbors = 15,
    initial_seed = 0.001,
    adopters_threshold = 0.4,
    social_influence = 0.7,
    quality = 0.5,
    number_of_consumers = 3000,
    activation_sharpness = 70,
    critical_mass = 0.50,
    marketing_effort = 0,
    level = 1
)


#==============================================================================
# Mapping of parameter names to the names in our article
#==============================================================================
article_parameters = dict(
    randomness = 'r',
    number_of_neighbors = 'k',
    adopters_threshold = 'h',
    social_influence = r'\beta',
    quality = 'q',
    number_of_consumers = 'N',
    activation_sharpness = r'\phi',
    critical_mass = 'M_c',
)

#==============================================================================
# Save parameters in a "Results" directory, placed next to this file
#==============================================================================
RESULTS_DIR = osp.join(LOCATION, 'Results')

# Create the directory
if not osp.isdir(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Create file name to save parameters
# It's going to be of the form main_parameter_#.txt
name = osp.join(RESULTS_DIR, main_parameter + '_')
number = len(glob.glob(name + '*.txt'))
filename = name + str(number) + '.txt'

# Save the run parameters in a dict
run = dict(
    main_parameter=main_parameter,
    parameter_values=parameter_values,
    number_of_times=number_of_times,
    max_time=max_time
)

# Create a dict with all the needed paramaters
all_parameters = dict(
    run=run,
    parameters=parameters
)

# Save all parameters
with open(filename, 'w') as f:
    json.dump(all_parameters, f, indent=4)


#==============================================================================
# Main variables
#==============================================================================
# Remove the parameter we want to study
parameters.pop(main_parameter)

# Direct view to the IPyparallel engines
rc = Client()
dview = rc[:]

# Global utility activation value
activation_value = compute_global_utility_activation_value(parameters)


#==============================================================================
# Simulation
#==============================================================================
# Generating different sets of parameters
set_of_parameters = generate_parameters(parameters, main_parameter,
                                        parameter_values)

# Reset the engines
get_ipython().magic('px %reset -f')  # analysis:ignore

# Run the simulation
data = []
for p in set_of_parameters:
    print(len(data))
    p_data = compute_run(number_of_times=number_of_times,
                         parameters=p,
                         max_time=max_time,
                         dview=dview)
    data.append(p_data)


#==============================================================================
# Plotting
#==============================================================================

fig_filename = osp.splitext(filename)[0] + '.png'

multiplot_adopters_and_global_utility(data=data,
                                      par_name=article_parameters[main_parameter],
                                      par_values=parameter_values,
                                      activation_value=activation_value,
                                      cumulative=True,
                                      filename=fig_filename,
                                      max_time=max_time)
