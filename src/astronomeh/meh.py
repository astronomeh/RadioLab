import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import scipy.stats as stats


# Capture and save data
def cap(fs=2e6,LO=1.420405e9,ns=4096,nb=2,fs_step=1e5,sweep_to=2e6,RF=None,dir=False):
	unixtime = time.time()
	to_datetime = datetime.datetime.fromtimestamp(unixtime)
	yyyymmdd = to_datetime.strftime("%Y_%m_%d")
	hhmmss = to_datetime.strftime("%H_%M_%S")
	path = os.path.join(os.getcwd(), yyyymmdd)
	path2 = os.path.join(path, hhmmss)
	for p in [path, path2]:
		os.makedirs(p, exist_ok=True)
	nfreq = 0
	datasum = 0
	all_data = []
	all_meta = []
	while fs <= sweep_to:		
		sdro = ugradio.sdr.SDR(direct=False,sample_rate=fs,center_freq=LO)
		time_start = time.time()
		data = sdro.capture_data(nsamples=ns,nblocks=nb)
		time_end = time.time()
		all_data.append(data)
        
		all_meta.append({
			'fs':fs,
			'LO':LO,
			'RF':RF,
			'ns':ns,
			'nb':nb,
			'ds':sdro.direct,
			'time':time.time(),
			'day':yyyymmdd,
			'run':hhmmss
			})
		sdro.close()
		print(f"Data captured for {fs/1e6} MHz sample rate. Took {time_end-time_start} seconds")
		datasum+=1
		fs+=fs_step
	all_data = np.stack(all_data, axis=0)
	np.savez(os.path.join(path2, hhmmss),data=all_data, metadata=np.array(all_meta, dtype=object))
	print(f"Data captured for {datasum} sample rates.")
	return all_data, all_meta


# Time Series Plot
def ts(data,meta=None,frange=None,show=False,save=False,blocks=1):
	if frange is None:
		frange = range(len(data))

	for f in frange:
		m = meta[f]
		path = os.path.join(os.getcwd(), f"{m['day']}")
		path2 = os.path.join(path, f"{m['run']}")
		path3 = os.path.join(path2, f"{m['fs']}")
		for p in [path,path2,path3]:
			os.makedirs(p, exist_ok=True)
		i = 1
		while i < blocks+1:
			this_data = data[f,i]
			this_data = this_data - np.mean(this_data)
			data_I = this_data[:,0]
			data_Q = this_data[:,1]
			x = np.linspace(0,m['ns']/m['fs'],m['ns'])
			data_I = np.reshape(data_I,x.shape)
			data_Q = np.reshape(data_Q,x.shape)
			z = data_I+1j*data_Q
			
			fig, ax = plt.subplots()
			ax.plot(x,data_I)
			ax.scatter(x,data_I)
			ax.set_xlim(0,0.00001)
			ax.set_xlabel("Time (s)")
			ax.set_ylabel("Amplitude")
			if m['RF'] is not None:
				ax.set_title(f"{m['RF']/1e9} GHz RF sampled at {m['fs']/1e6} MHz with {m['LO']/1e9} GHz LO")
			else:
				ax.set_title(f"Noise signal sampled at {m['fs']/1e6} MHz Block {i+1}")
			fig.savefig(os.path.join(path3, f"signal_plot_{m['fs']/1e6}MHz_block{i+1}.png"), bbox_inches="tight")
			plt.close()
			i+=1
			
	print(data.shape)
	if meta is not None:
		for i, m in enumerate(meta):
			print(f"The shape of the data for {m['fs']/1e6} MHz scan is {data[i].shape}.")
	
def pow(data,meta,frange=None,show=False,save=True):
	path = os.path.join(os.getcwd(), yyyymmdd)
	path2 = os.path.join(path, hhmmss)
	for p in [path, path2]:
		os.makedirs(p, exist_ok=True)
	if frange is None:
		for f, m in enumerate(meta):
			i = 1
			while i < m['nb']:
				this_data = data[f,i]
				this_data = this_data - np.mean(this_data)
				data_I = this_data[:,0]
				data_Q = this_data[:,1]
				x = np.linspace(0,m['ns']/m['fs'],ns)
				data_I = np.reshape(data_I,x.shape)
				data_Q = np.reshape(data_Q,x.shape)
				z = data_I+1j*data_Q
