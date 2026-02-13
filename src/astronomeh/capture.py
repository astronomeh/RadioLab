import os
import ugradio
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import scipy.stats as stats

fs = 2.0e6                        # Sample Rate in Hz
RF = None                         # Target in Hz
LO = 1500e6                   # Local Oscillator in Hz
sweep_to = 2.0e6                  # Sweep fs from fs to sweep_to
nb = 100                          # nblocks in SDR capture
ns = 20480	                  # nsamples per block
T =    ns/fs                      # Time length of block
unix_time = time.time()           # Get capture time

to_datetime = datetime.datetime.fromtimestamp(unix_time)
yyyymmdd = to_datetime.strftime("%Y_%m_%d")
hhmmss = to_datetime.strftime("%H_%M_%S")
parent_directory = os.getcwd()
path = os.path.join(parent_directory, yyyymmdd)
path2 = os.path.join(path, hhmmss)
for p in [path, path2]:
        os.makedirs(p, exist_ok=True)
nfreq = 0
datasum = 0

while fs <= sweep_to:
        sdro = ugradio.sdr.SDR(direct=False,sample_rate=fs,center_freq=LO)
        data = sdro.capture_data(nsamples=ns,nblocks=nb)
        i = 1
        # For multiple blocks
        while i < nb:
                print(f"data captured for block {i}")
                data_I = data[i,:,0]
                data_Q = data[i,:,1]
                file_name = f"LOat{LO}_FSat{fs}"
                full_path = os.path.join(path2, file_name)
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
                
                x = np.linspace(0,T,ns)
                #sinx = 20*np.sin(RF*T) # Trying to make theoretical wave at RF
                data_I = np.reshape(data_I,x.shape)
                data_Q = np.reshape(data_Q,x.shape)
                z = data_I+1j*data_Q

                '''
                fig, ax = plt.subplots()
                ax.plot(x,data_I)

                #ax.plot(x,sinx)
                ax.scatter(x,data_I)
                ax.set_xlim(0,0.00001)
                #ax.set_ylim(-150,150)

                ax.set_title(f"{RF/1e6} MHz RF sampled at {fs/1e6} MHz with {LO/1e6} MHz LO")
                #ax.set_title(f"Noise signal sampled at {sample_freq} Hz Window {i}")
                #ax.set_title(f"Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
                                
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Amplitude")
                file_name = f"signal_plot_{fs}.png"
                full_path = os.path.join(path2, file_name)
                fig.savefig(full_path, bbox_inches="tight")
                '''
               
                
                fft_data = np.fft.fft(z)
                ts = 1/fs
                

                freq = np.fft.fftfreq(ns,d=ts)
                x2 = np.fft.fftshift(freq)
                fft_data = np.fft.fftshift(fft_data)

                '''
                fig, ax = plt.subplots()
                ax.plot(x2,fft_data.imag,label="Imaginary")
                ax.plot(x2,fft_data.real,label="Real")
                #ax.plot(freq,V_rms)
                ax.axvline(x=fs/2, linestyle = '--')
                ax.axvline(x=-fs/2, linestyle = '--')
                ax.axvline(x=0, linestyle = '--')
                
                ax.set_title(f"Voltage Spectrum of {RF/1e6} MHz RF sampled at {fs/1e6} MHz with {LO/1e6} MHz LO")
                #ax.set_title(f"Voltage Spectrum of Noise signal sampled at {sample_freq} Hz")
                #ax.set_title(f"Voltage Spectrum of Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
                        
                ax.set_xlabel("Frequency (Hz)")
                ax.set_ylabel("Voltage")
                file_name = f"voltage_spectrum_{fs}.png"
                full_path = os.path.join(path2, file_name)
                fig.savefig(full_path, bbox_inches="tight")
                plt.close(fig)
                print("voltage spectrum created")
        
                '''
                mask = x2>=0
                power = np.abs(fft_data)**2

                datasum+=power
                '''
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
                ax.axvline(x=fs/2, linestyle = '--')
                ax.axvline(x=-fs/2, linestyle = '--')
                ax.axvline(x=0, linestyle = '--')

        #Titles
                ax.set_title(f"Power Spectrum of {RF/1e6} MHz RF sampled at {fs/1e6} MHz with {LO/1e6} MHz LO")
                #ax.set_title(f"Power Spectrum of Noise signal sampled at {sample_freq} Hz")
                #ax.set_title(f"Power Spectrum of Mixed {signal_freq} MHz and {signal_freq2} MHz signal sampled at {sample_freq} Hz")
                
                ax.set_xlabel("Frequency (Hz)")
                ax.set_ylabel("Power")
                ax.set_yscale("log")

                ax.grid()
                file_name = f"power_spectrum_{fs}.png"
                full_path = os.path.join(path2, file_name)
                fig.savefig(full_path, bbox_inches="tight")
                plt.xlim(.67e6,.73e6)
                file_name = f"power_spectrum_{fs}_zoomed.png"
                full_path = os.path.join(path2, file_name)
                fig.savefig(full_path, bbox_inches="tight")
                plt.close(fig)
                print("power spectrum created")
                '''
                i+=1

        fig, ax = plt.subplots()

        ax.plot(x2,datasum)
        plt.scatter(x2,datasum, color="red",s=5)
        ax.axvline(x=fs/2, linestyle = '--')
        ax.axvline(x=-fs/2, linestyle = '--')
        ax.axvline(x=0, linestyle = '--')

        if RF is not None:
                ax.set_title(f"Total Power Spectrum of {RF/1e6} MHz RF sampled at {fs/1e6} MHz with {LO/1e6} MHz LO ({nb} blocks")
        else:
                ax.set_title(f"Total Power Spectrum of {nb} blocks sampled at {fs/1e6} MHz with {LO/1e6} MHz LO")

        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power")
        ax.set_yscale("log")

        ax.grid()
        file_name = f"total_power_spectrum_{fs}.png"
        full_path = os.path.join(path2, file_name)
        fig.savefig(full_path, bbox_inches="tight")
        plt.xlim(.40e6,0.60e6)
        file_name = f"total_power_spectrum_{fs}_zoomed.png"
        full_path = os.path.join(path2, file_name)
        fig.savefig(full_path, bbox_inches="tight")
        plt.close(fig)
        print("total power spectrum created")

        fs+=1e5   # 0.1MHz steps for sweep









  
