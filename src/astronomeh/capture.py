import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import scipy.stats as stats

fs = 2.0e6                        # Sample Rate in Hz
RF = 1420.405e6                        # Target in Hz
LO = 1420.905e6                         # Local Oscillator in Hz
sweep_to = 2.0e6                  # Sweep fs from fs to sweep_to
nb = 2                            # nblocks in SDR capture
ns = 4096	                        # nsamples in SDR capture
unix_time = time.time()           # Get capture time

to_datetime = datetime.datetime.fromtimestamp(unix_time)
yyyymmdd = to_datetime.strftime("%Y%m%d")
parent_directory = os.getcwd()
output_folder = f"{yyyymmdd[:4]}_{yyyymmdd[4:6]}_{yyyymmdd[6:]}"
path = os.path.join(parent_directory, output_folder)
os.makedirs(path, exist_ok=True)
nfreq = 0
datasum = 0

def capture(fs,RF,LO,sweep_to,nb,ns,unix_time):
  while fs <= sweep_to:
    sdro = ugradio.sdr.SDR(direct=True,sample_rate=fs,center_freq=Lo)
    data = sdro.capture_data(nsamples=ns,nblocks=nb)
    file_name = f"LOat{LO}_FSat{fs}"
    full_path = os.path.join(path, file_name)
  	metadata = {
  		'sample frequency':f'{fs}',
  		'signal frequency LO':f'{LO}',
  		'signal frequency RF':f'{RF}',
      'number of samples per block':f'{ns}',
      'number of blocks':f'{nb}',
  		'direct sampling':f'{sdro.direct}',
      'unix time':f'{unix_time}'
  	}
  	np.savez(full_path,data, attributes=metadata)
    sdro.close()
    fs+=1e5   # 0.1MHz steps for sweep


	











  
