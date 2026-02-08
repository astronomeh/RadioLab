import numpy as np
import matplotlib.pyplot as plt



# Package Installation Test
def test():
  print("Hello Professor!")



# Create time plot
def plot_time(data,signal_freq,signal_freq2,sample_freq,split,direct,N):
  
  # Length of observation
  T = N/sample_freq

  # Time axis
  x = np.linspace(0,T,N)
  
  # For Complex Data
  if not direct:
    # Separate Complex Components
    in_phase = data[1,:,0]
    quad = data[1,:,1]

    # Plot
    plt.figure()
    plt.plot(x,in_phase,c="green",label="In-Phase")
    plt.scatter(x,in_phase,c="green",s=5)
    plt.plot(x,quad,c="red",label="Quadrature")
    plt.scatter(x,quad,c="red",label="Quadrature",s=5)
    plt.xlim(0,1e-5)
    
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
    plt.title(f"Mixed {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")

  plt.show()



# Create Voltage Spectrum
def plot_volt(data,signal_freq,signal_freq2,sample_freq,split,direct):

  # Set Title
  if signal_freq2 == Empty:
    plt.title(f"{signal_freq} Mhz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Combined {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")
  else:
    plt.title(f"Mixed {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")



# Create Power Spectrum
def plot_pow(data,signal_freq,signal_freq2,sample_freq,split,direct):

  # Set Title
  if signal_freq2 == Empty:
    plt.title(f"{signal_freq} Mhz Signal Sampled at {sample_freq/1e6} Mhz")
  elif split:
    plt.title(f"Combined {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")
  else:
    plt.title(f"Mixed {signal_freq} Mhz and {signal_freq2} Mhz Signal sampled at {sample_freq/1e6} Mhz")

