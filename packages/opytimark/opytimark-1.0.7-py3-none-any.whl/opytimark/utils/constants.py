"""Constants.
"""

import sys

# Defines where data should be downloaded and loaded
DATA_FOLDER = 'data/'

# A constant value used to avoid division by zero, zero logarithms
# and any possible mathematical error
EPSILON = 1e-32

# When the agents are initialized, their fitness is defined as
# the maximum float value possible
FLOAT_MAX = sys.float_info.max
