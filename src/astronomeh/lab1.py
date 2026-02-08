import numpy as np
import matplotlib.pyplot as plt



# Package Installation Test
def test():
  print("Hello Professor!")



# Create time plot
def plot_time(data=None,usbdata=None,lsbdata=None,signal_freq,signal_freq2=None,usb_freq=None,Lsb_freq=None,sample_freq,split,direct,N):
  
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
    plt.plot(x,usbin_phase,c="black",label="USB In-Phase")
    plt.scatter(x,usbin_phase,c="black",s=5)
    plt.plot(x,lsbin_phase,c="black","--",label="LSB In-Phase")
    plt.scatter(x,lsbin_phase,c="black",s=5)
    plt.plot(x,usbquad,c="green",label="USB Quadrature")
    plt.scatter(x,usbquad,c="green",s=5)
    plt.plot(x,lsbquad,c="red",label="LSB Quadrature")
    plt.scatter(x,lsbquad,c="red",s=5)
    plt.xlim(0,1e-5)
    plt.legend(loc="upper right")
    
  # For Real Data
  else:
    data=data[1]
    
    # Plot
    plt.figure()
    plt.plot(x,data,c="black")
    plt.scatter(x,data,c="red",s=5)

  

  
  # Set Title
  if signal_freq2 == None:
    plt.title(f"{signal_freq} Mhz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Combined {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")
  else:
    plt.title(f"Mixed {signal_freq} Mhz LO and {usb_freq}/{lsbfreq} Mhz RF Signals sampled at {sample_freq/1e6} Mhz")
  plt.grid()
  plt.xlabel("Time (1e-5 s)")
  plt.ylabel("Amplitude (Arbitrary Voltage Units)")
  plt.show()



# Create Voltage Spectrum
def plot_volt(data,signal_freq,signal_freq2,sample_freq,split,direct):

  # Set Title
  if signal_freq2 == Empty:
    plt.title(f"Voltage Spectrum of {signal_freq} Mhz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Voltage Spectrum of Combined {signal_freq} Mhz and {signal_freq2} Mhz Signal")
  else:
    plt.title(f"Voltage Spectrum of Mixed {signal_freq} Mhz LO and {signal_freq2} Mhz RF Signal")



# Create Power Spectrum
def plot_pow(data,signal_freq,signal_freq2,sample_freq,split,direct):

  # Set Title
  if signal_freq2 == Empty:
    plt.title(f"Power Spectrum of {signal_freq} Mhz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Power Spectrum of Combined {signal_freq} Mhz and {signal_freq2} Mhz Signal")
  else:
    plt.title(f"Power Spectrum of Mixed {signal_freq} Mhz LO and {signal_freq2} Mhz RF Signal")
