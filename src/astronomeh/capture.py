import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import scipy.stats as stats

fs = 1.0e6                        # Sample Rate in Hz
RF = 1.5e6                        # Target in Hz
LO = 30                           # Local Oscillator in Hz
sweep_to = 3.2e6                  # Sweep fs from fs to sweep_to
nb = 2                            # nblocks in SDR capture
ns = 4096	                        # nsamples in SDR capture
unix_time = time.time()           # Get capture time
to_datetime = datetime.datetime.fromtimestamp(unix_time)

yyyymmdd = to_datetime.strftime("%Y%m%d")
parent_directory = os.getcwd()
output_folder = f"{yyyymmdd[:4]}_{yyyymmdd[4:6]}_{yyyymmdd[6:]}"
path = os.path.join(parent_directory, output_folder)



