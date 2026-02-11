import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.stats as stats

sample_freq = 1.0e6 #Hz
signal_freq = 1.5 #MHz
signal_freq2 = 30
nb = 2 																	#capture_data nblocks
ns = 4096																#capture_data nsamples

parent_directory = os.getcwd()
path = os.path.join(parent_directory, "output")
path2 = os.path.join(path,"data")
path3 = os.path.join(path,"plots")
path4 = os.path.join(path3,"signal")
path5 = os.path.join(path3,"voltage_spectrum")
path6 = os.path.join(path3,"power_spectrum")
path7 = os.path.join(path3, "small_gap")
path8 = os.path.join(path7, "average")
path9 = os.path.join(path4,"zoomed")
path10 = os.path.join(path6,"zoomedcarrier")
path11 = os.path.join(path6,"zoomeddif")
path12 = os.path.join(path2,"Quadrature")

for p in [path, path2, path3, path4, path5, path6, path7, path8, path9, path10, path11, path12]:
    os.makedirs(p, exist_ok=True)
nfreq = 0
datasum = 0
  
while sample_freq <= 3.2e6:
# Time
	T = ns/sample_freq
	
# Create SDR Object.
	sdr = ugradio.sdr.SDR(direct=True,sample_rate=sample_freq,center_freq=29e6)
# Capture data
	the_data = sdr.capture_data(nsamples=ns,nblocks = nb)
	print(the_data[1])
	print("data successfully collected for", sample_freq)
	file_name = f"digital_sin_{sample_freq}.npy"
	full_path = os.path.join(path2, file_name)
	metadata = {
		'sample frequency':f'{sample_freq}',
		'signal frequency LO':f'{signal_freq}',
		'signal frequency RF':f'{signal_freq2}',
		'direct sampling':f'{sdr.direct}'
	}
	np.savez(full_path,the_data, attributes=metadata)
	
	
	if sdr.direct:
		sdr.close()
		in_phase = the_data
		quad = None
		z = in_phase.astype(float)
	else:
		sdr.close()
		in_phase = the_data[:,:,0]
		quad = the_data[:,:,1]
		z = in_phase.astype(float) + 1j*quad.astype(float)
		
	
	print(z.shape)
	print(z[1])
# Dump buffer block at i=0
	i=1
	means=[]
# For multiple blocks, nb > 2
	while i <=(nb-1):
		print(z.shape)
		data = z[i]
		print(z[i,:])
		datasum += data

# Plot Time domain signal
		x = np.linspace(0,T,ns)
		#sinx = 1000000*np.sin(x/500000)
		fig, ax = plt.subplots()
		ax.plot(x,data)
		#ax.plot(x,sinx)
		ax.scatter(x,data)
		ax.set_xlim(0,0.0001)
		#ax.set_ylim(-150,150)
		
# Titles
		ax.set_title(f"{signal_freq} MHz signal sampled at {sample_freq} Hz")
		#ax.set_title(f"Noise signal sampled at {sample_freq} Hz Window {i}")
		#ax.set_title(f"Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
		
		ax.set_xlabel("Time (s)")
		ax.set_ylabel("Amplitude")
		file_name = f"signal_plot_{sample_freq}_{i}.png"
		full_path = os.path.join(path4, file_name)
		fig.savefig(full_path, bbox_inches="tight")
# Zoom in
		ax.set_xlim(0,0.00002)
		full_path = os.path.join(path9, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.close(fig)
		print("signal plot created")
		
	
# Plot Voltage Spectrum

# Fast Fourier Transform
		fft_data = np.fft.fft(data)
		timestep = 1/sample_freq
		freq = np.fft.fftfreq(ns,d=timestep)
		freqs = np.fft.fftshift(freq)
		fft_data = np.fft.fftshift(fft_data)
		#x=data-np.mean(data)
		#w = np.hanning(n)
		#xw = x*w
		#coherent_gain = np.mean(w)
		#U = np.mean(w**2)
		#X = np.fft.rfft(xw)
		
		#V_peak = (2.0/(n*coherent_gain))*np.abs(X)
		#V_peak[0] = (1.0/(n*coherent_gain))*np.abs(X[0])
		#if n%2==0:
		#	V_peak[-1] = (1.0/(n*coherent_gain))*np.abs(X[-1])
		#V_rms = V_peak/np.sqrt(2.0)
		
		fig, ax = plt.subplots()
		x2=freqs
		ax.plot(x2,fft_data.imag,label="Imaginary")
		ax.plot(x2,fft_data.real,label="Real")
		#ax.plot(freq,V_rms)
		ax.axvline(x=sample_freq/2, linestyle = '--')
		ax.axvline(x=-sample_freq/2, linestyle = '--')
		ax.axvline(x=0, linestyle = '--')
# Titles
		ax.set_title(f"Voltage Spectrum of {signal_freq} MHz signal sampled at {sample_freq} Hz")
		#ax.set_title(f"Voltage Spectrum of Noise signal sampled at {sample_freq} Hz")
		#ax.set_title(f"Voltage Spectrum of Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
		
		ax.set_xlabel("Frequency (Hz)")
		ax.set_ylabel("Voltage")
		file_name = f"voltage_spectrum_{sample_freq}.png"
		full_path = os.path.join(path5, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.close(fig)
		print("voltage spectrum created")
			
# Power Spectrum
		mask = x2>=0
		power = np.abs(fft_data**2)
		idx = np.argsort(power)
		sortedpower = x2[idx]
		#n2=0
		#res = sortedpower[-n:]
		fig, ax = plt.subplots()
		#while n2 <= 19:
		#	p_max = res[n2]
		#	ax.axvline(x=res[n], linestyle = '--', color="red")
		#	ax.text(p_max, ax.get_ylim()[1],f"{p_max} Hz", rotation = 90, va="top", ha="right")
		#	n2+=1
	
		ax.plot(x2,power)
		plt.scatter(x2,power, color="red",s=5)
		ax.axvline(x=sample_freq/2, linestyle = '--')
		ax.axvline(x=-sample_freq/2, linestyle = '--')
		ax.axvline(x=0, linestyle = '--')

#Titles
		ax.set_title(f"Power Spectrum of {signal_freq} MHz signal sampled at {sample_freq} Hz")
		#ax.set_title(f"Power Spectrum of Noise signal sampled at {sample_freq} Hz")
		#ax.set_title(f"Power Spectrum of Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
		
		ax.set_xlabel("Frequency (Hz)")
		ax.set_ylabel("Power")
		ax.set_yscale("log")
	
		ax.grid()
		file_name = f"power_spectrum_{sample_freq}.png"
		full_path = os.path.join(path6, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.xlim(.67e6,.73e6)
		full_path = os.path.join(path10, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.xlim(-1e5,1e5)
		full_path = os.path.join(path11, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.close(fig)
		print("power spectrum created")

# Inverse Fourier Transform	
		inverse_power = np.fft.ifft(power)
		fig, ax = plt.subplots()
		ax.plot(x,inverse_power)
		#ax.axvline(x=p_max, linestyle = '--', color="red")
		ax.set_title(f"Inverse Transform of Power Spectrum of {signal_freq} Hz signal sampled at {sample_freq} Hz")
		ax.set_xlabel("Time (s)")
		ax.set_ylabel("Amplitude")
		ax.set_xlim(0,0.00002)
		#ax.set_yscale("log")
		#ax.text(p_max, ax.get_ylim()[1],f"{p_max} Hz", rotation = 90, va="top", ha="right")
		#ax.text(sample_freq/2, ax.get_ylim()[1],f"{sample_freq/2} Hz", rotation = 90, va="top", ha="right")
		file_name = f"inverse_power_spectrum_{sample_freq}.png"
		full_path = os.path.join(path6, file_name)
		fig.savefig(full_path, bbox_inches="tight")
		plt.close(fig)
		print("inverse power spectrum created")



	
		#volt_spectrum = np.fft.fft(data)
		#power_spectrum = volt_spectrum * np.conj(volt_spectrum)
		#auto_correlation = np.correlate(volt_spectrum,volt_spectrum, mode = "same")
		#plt.figure()
		#plt.plot(x, power_spectrum)
		#plt.plot(x, auto_correlation)
		#plt.title(f"Auto-correlation of Voltage signal at {signal_freq} Hz sampled at {sample_freq} Hz")
		#plt.xlabel("Frequency")
		#plt.ylabel("Auto Correlation")
		#plt.yscale("log")
		#file_name = f"auto_correlation_{sample_freq}.png"
		#full_path = os.path.join(os.path.join(path3,"auto_correlation"),file_name)
		#plt.savefig(full_path)
		#plt.close()
		#print("auto correlation created")
	

		extra_length_voltage_dft = ugradio.dft.dft(data, vsamp = sample_freq, f = np.linspace(-2*sample_freq,2*sample_freq,ns))
		x = extra_length_voltage_dft[0]
		extra_length_power_spectrum = np.abs(extra_length_voltage_dft[1]) ** 2
		plt.figure()
		plt.plot(x, np.fft.fftshift(extra_length_power_spectrum))
		plt.scatter(x, np.fft.fftshift(extra_length_power_spectrum), color="red",s=5)
		plt.axvline(0,ls="--",c="red")
		plt.axvline(sample_freq/2,ls="--",c="red")
		plt.axvline(3*sample_freq/2,ls="--",c="red")
		plt.axvline(2*sample_freq,ls="--",c="red")
		plt.axvline(-sample_freq/2,ls="--",c="red")
		plt.axvline(-3*sample_freq/2,ls="--",c="red")
		plt.axvline(-2*sample_freq,ls="--",c="red")
		plt.axvline(-sample_freq,ls="--",c="red")
		plt.axvline(sample_freq,ls="--",c="red")
		plt.title(f"Power spectrum with small frequency separation at {signal_freq} Hz samples at {sample_freq} Hz")
		#plt.title(f"Power spectrum with small frequency separation of Noise samples at {sample_freq} Hz")
		plt.yscale("log")
		plt.xlabel("Frequencies")
		#plt.xlim(.49e6,.51e6)
		plt.xlim(-sample_freq/2,sample_freq/2)
		plt.ylabel("Magnitude")
		plt.ticklabel_format(axis="x",style="sci",scilimits=(0,0))
		plt.grid()
		file_name = f"small_gap_{sample_freq}_{i}.png"
		full_path = os.path.join(path7, file_name)
		plt.savefig(full_path)
		plt.close()
		
		
		print("dft created")

		mean = np.mean(data)
		means.append(mean)
		print("Mean =",mean)
		variance = np.var(data)
		print("Variance =",variance)
		
		sigma = np.sqrt(variance)
		#rms = np.sqrt(np.mean(data**2))
		#print(rms)
		"""
		plt.figure()
		x=np.linspace(-45,45,100)
		
		
		plt.hist(data,bins="auto",density="True")
		plt.plot(x, stats.norm.pdf(x,mean, sigma))
		file_name = f"Noise Histogram Sampled at {sample_freq}_{i}.png"
		full_path = os.path.join(path3,file_name)
		plt.savefig(full_path)
		plt.close()
		"""
		print("Wait")
		time.sleep(.01)
		i+=1
	total_mean = np.mean(means)
	print(total_mean)
	
	extra_length_voltage_dft = ugradio.dft.dft(datasum/nb, vsamp = sample_freq, f = np.linspace(-2*sample_freq,2*sample_freq,ns))
	x = extra_length_voltage_dft[0]
	extra_length_power_spectrum = np.abs(extra_length_voltage_dft[1]) ** 2
	plt.figure()
	plt.plot(x, np.fft.fftshift(extra_length_power_spectrum))
	plt.scatter(x, np.fft.fftshift(extra_length_power_spectrum), color="red",s=5)
	plt.axvline(0,ls="--",c="red")
	plt.axvline(sample_freq/2,ls="--",c="red")
	plt.axvline(3*sample_freq/2,ls="--",c="red")
	plt.axvline(2*sample_freq,ls="--",c="red")
	plt.axvline(-sample_freq/2,ls="--",c="red")
	plt.axvline(-3*sample_freq/2,ls="--",c="red")
	plt.axvline(-2*sample_freq,ls="--",c="red")
	plt.axvline(-sample_freq,ls="--",c="red")
	plt.axvline(sample_freq,ls="--",c="red")
	
	plt.title(f"Power spectrum with small frequency separation at {signal_freq} MHz samples at {sample_freq} Hz")
	#plt.title(f"Power spectrum with small frequency separation of Noise samples at {sample_freq} Hz")
	
	#plt.yscale("log")
	plt.xlabel("Frequencies")
	#plt.xlim(.49e6,.51e6)
	plt.xlim(-sample_freq/2,sample_freq/2)
	plt.ylabel("Magnitude")
	plt.ticklabel_format(axis="x",style="sci",scilimits=(0,0))
	plt.grid()
	file_name = f"small_gap_{sample_freq}_Average.png"
	full_path = os.path.join(path8, file_name)
	plt.savefig(full_path)
	plt.close()
		
		
	sample_freq += 1.0e5
	nfreq += 1
print(f"Sweep Completed. {nfreq} frequencies checked.")
