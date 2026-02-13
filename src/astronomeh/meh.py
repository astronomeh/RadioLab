import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import scipy.stats as stats

def capture(fs,LO,ns,nb,time=time.time(),fs_step=1e5,sweep_to=2e6,RF=None,dir=False):
	to_datetime = datetime.datetime.fromtimestamp(time)
	yyyymmdd = to_datetime.strftime("%Y_%m_%d")
	hhmmss = to_datetime.strftime("%H_%M_%S")
	parent_directory = os.getcwd()
	path = os.path.join(parent_directory, yyyymmdd)
	path2 = os.path.join(path, hhmmss)
	for p in [path, path2]:
        os.makedirs(p, exist_ok=True)
	nfreq = 0
	datasum = 0
	all_data = []
	all_meta = []
	while fs <= sweep_to:
        sdro = ugradio.sdr.SDR(direct=False,sample_rate=fs,center_freq=LO)
        data = sdro.capture_data(nsamples=ns,nblocks=nb)
		all_data.append(data)
        
        all_meta.append({
                'sample frequency':f'{fs}',
                'signal frequency LO':f'{LO}',
                'signal frequency RF':f'{RF}',
                'number of samples per block':f'{ns}',
                'number of blocks':f'{nb}',
                'direct sampling':f'{sdro.direct}',
                'unix time':f'{time.time()}'
                })
        sdro.close()
		print(f"Data captured for {fs/1e6} MHz sample rate.")
		datasum+=1
		fs+=fs_step
	all_data = np.stack(all_data, axis=0)
	np.savez(os.path.join(path2, hhmmss),data=all_data, metadata=np.array(all_meta, dtype=object))
	print(f"Data captured for {datasum} sample rates.")
	return(all_data)

def ts(data):
	print(data.shape)
