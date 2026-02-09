import numpy as np
import matplotlib.pyplot as plt



# Package Installation Test
def test():
  print("Hello Professor!")



# Create time plot
def plot_time(signal_freq,sample_freq,split,direct,N,data=None,usbdata=None,lsbdata=None,signal_freq2=None,usb_freq=None,lsb_freq=None):
  
  # Length of observation
  T = N/sample_freq

  # Time axis
  x = np.linspace(0,T,N)
  
  # For Complex Data
  if not direct:
    # Separate Complex Components
    usbin_phase = usbdata[1,:,0]
    usbquad = usbdata[1,:,1]
    lsbin_phase = lsbdata[1,:,0]
    lsbquad = lsbdata[1,:,1]
    # Plot
    plt.figure()
    plt.plot(x,lsbin_phase,c="black",label="In-Phase",ls="--")
    plt.scatter(x,lsbin_phase,c="black",s=5)
    plt.plot(x,usbquad,c="cornflowerblue",label=f"USB Quadrature {usb_freq}MHz")
    plt.scatter(x,usbquad,c="cornflowerblue",s=5)
    plt.plot(x,lsbquad,c="red",label=f"LSB Quadrature {lsb_freq}MHz")
    plt.scatter(x,lsbquad,c="red",s=5)
    plt.xlim(0,5e-6)
    plt.legend(loc="upper right")
    
  # For Real Data
  else:
    data=data[1]
    
    # Plot
    plt.figure()
    plt.plot(x,data,c="black")
    plt.scatter(x,data,c="red",s=5)

  

  
  # Set Title
  if signal_freq2 == None and usb_freq == None:
    plt.title(f"{signal_freq} MHz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Combined {signal_freq} MHz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")
  else:
    plt.title(f"Mixed {signal_freq} MHz LO and {lsb_freq}/{usb_freq} Mhz RF Signals sampled at {sample_freq/1e6} Mhz")
  plt.grid()
  plt.xlabel("Time (1e-6 s)")
  plt.ylabel("Amplitude (Arbitrary Voltage Units)")
  plt.show()



# Create Voltage Spectrum
def plot_volt(data,signal_freq,signal_freq2,sample_freq,split,direct):

  # Set Title
  if signal_freq2 == None and usb_freq == None:
    plt.title(f"Voltage Spectrum of {signal_freq} MHz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Voltage Spectrum of Combined {signal_freq} MHz and {signal_freq2} Mhz Signal")
  else:
    plt.title(f"Voltage Spectrum of Mixed {signal_freq} MHz LO and {signal_freq2} Mhz RF Signal")



# Create Power Spectrum
def plot_pow(signal_freq,sample_freq,split,direct,N,data=None,usbdata=None,lsbdata=None,signal_freq2=None,usb_freq=None,lsb_freq=None):
  if not direct:
    usbin_phase = usbdata[1,:,0]
    usbquad = usbdata[1,:,1]
    lsbin_phase = lsbdata[1,:,0]
    lsbquad = lsbdata[1,:,1]

    usbz = usbin_phase+1j*usbquad
    lsbz = lsbin_phase+1j*lsbquad

    usbfft = np.fft.fft(usbz)
    lsbfft = np.fft.fft(lsbz)
    ts = 1/sample_freq
    usbfreq = np.fft.fftfreq(N,d=ts)
    usbfreq = np.fft.fftshift(usbfreq)
    usbfft = np.fft.fftshift(usbfft)
    lsbfreq = np.fft.fftfreq(N,d=ts)
    lsbfreq = np.fft.fftshift(lsbfreq)
    lsbfft = np.fft.fftshift(lsbfft)

    usbx = usbfreq
    lsbx = lsbfreq

    usbmask = usbx>=0
    lsbmask = lsbx>=0
    usbpow = np.abs(usbfft)**2
    lsbpow = np.abs(lsbfft)**2

    plt.plot(usbx/1e6, usbpow,c="cornflowerblue",alpha=0.7,label=f"USB {usb_freq}MHz")
    plt.scatter(usbx/1e6, usbpow,c="cornflowerblue", s=5)
    plt.plot(lsbx/1e6, lsbpow,c="red", alpha=0.7,label=f"LSB {lsb_freq}MHz")
    plt.scatter(lsbx/1e6, lsbpow,c="red",s=5)
    plt.axvline(x=-sample_freq/2e6,c="black",ls="--")
    plt.axvline(x=sample_freq/2e6,c="black",ls="--")
    plt.axvline(x=0,c="black")
    plt.yscale("log")
    plt.legend(loc="lower left")
    
    
  else:
    data = data[1]
    
  # Set Title
  if signal_freq2 == None and usb_freq == None:
    plt.title(f"Power Spectrum of {signal_freq} MHz Signal Sampled at {sample_freq/1e6} MHz")
  elif split:
    plt.title(f"Power Spectrum of Combined {signal_freq} MHz and {signal_freq2} Mhz Signal")
  else:
    plt.title(f"Power Spectrum of Mixed {signal_freq} MHz LO and {lsb_freq}/{usb_freq} Mhz RF Signals")
  plt.xlabel("Frequency (MHz)")
  plt.ylabel("log Power (Arbitrary Units)")
  plt.grid()
  plt.show()
