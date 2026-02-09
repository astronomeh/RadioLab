import numpy as np
import matplotlib.pyplot as plt


# Package Installation Test
def test():
  print("Hello Professor!")


# Create time plot
def plot_time(signal_freq,sample_freq=3e6,split=False,N=4096,data=None,usbdata=None,lsbdata=None,signal_freq2=None,usb_freq=None,lsb_freq=None,ax=None,show=False):
  if ax is None:
    fig, ax = plt.subplots()
  # Length of observation
  T = N/sample_freq
  
  # Time axis
  x = np.linspace(0,T,N)
  
  # For Complex Data
  if usb_freq is not None:
    # Separate Complex Components
    usbin_phase = usbdata[1,:,0]
    usbquad = usbdata[1,:,1]
    lsbin_phase = lsbdata[1,:,0]
    lsbquad = lsbdata[1,:,1]
    # Plot
    ax.plot(x,lsbin_phase,c="black",label="In-Phase",ls="--")
    ax.scatter(x,lsbin_phase,c="black",s=5)
    ax.plot(x,usbquad,c="cornflowerblue",label=f"USB Quadrature {usb_freq}MHz")
    ax.scatter(x,usbquad,c="cornflowerblue",s=5)
    ax.plot(x,lsbquad,c="red",label=f"LSB Quadrature {lsb_freq}MHz")
    ax.scatter(x,lsbquad,c="red",s=5)
    ax.set_xlim(0,5e-6)
    ax.legend(loc="upper right")
    
  # For Real Data
  else:
    data=data[1]
    
    # Plot
    ax.plot(x,data,c="black")
    ax.scatter(x,data,c="red",s=5)
  
  # Set Title
  if signal_freq2 == None and usb_freq == None:
    ax.set_title(f"{signal_freq}MHz Signal Sampled at {sample_freq/1e6}Mhz")
  elif split:
    ax.set_title(f"Combined {signal_freq}MHz and {signal_freq2}Mhz Signal sampled at {sample_freq/1e6}Mhz")
  else:
    ax.set_title(f"Mixed {signal_freq}MHz LO and {lsb_freq}/{usb_freq}Mhz RF Signals sampled at {sample_freq/1e6}Mhz")
  ax.grid(True)
  ax.set_xlabel("Time (1e-6 s)")
  ax.set_ylabel("Amplitude (Arbitrary Voltage Units)")

# Create Voltage Spectrum
def plot_volt(signal_freq,sample_freq,split=False,N=4096,data=None,usbdata=None,lsbdata=None,signal_freq2=None,usb_freq=None,lsb_freq=None,ax=None,show=False):

  # Set Title
  if signal_freq2 == None and usb_freq == None:
    ax.set_title(f"Voltage Spectrum of {signal_freq}MHz Signal Sampled at {sample_freq/1e6}Mhz")
  elif split:
    ax.set_title(f"Voltage Spectrum of Combined {signal_freq}MHz and {signal_freq2}Mhz Signal")
  else:
    ax.set_title(f"Voltage Spectrum of Mixed {signal_freq}MHz LO and {signal_freq2/1e6}Mhz RF Signal")



# Create Power Spectrum
def plot_pow(signal_freq, sample_freq=3e6, split=False, N=4096,data=None, usbdata=None, lsbdata=None, signal_freq2=None,usb_freq=None, lsb_freq=None, ax=None, show=False):

  if ax is None:
    fig, ax = plt.subplots()

  if usb_freq is not None:
    usbdata_arr = np.asarray(usbdata)
    lsbdata_arr = np.asarray(lsbdata)

    if usbdata_arr.ndim == 3 and usbdata_arr.shape[-1] >= 2:
      usbin_phase = np.asarray(usbdata_arr[1, :, 0]).ravel()
      usbquad = np.asarray(usbdata_arr[1, :, 1]).ravel()
      lsbin_phase = np.asarray(lsbdata_arr[1, :, 0]).ravel()
      lsbquad = np.asarray(lsbdata_arr[1, :, 1]).ravel()
      usbz = usbin_phase + 1j * usbquad
      lsbz = lsbin_phase + 1j * lsbquad
    else:
      usbz = np.asarray(usbdata_arr[1, :]).ravel()
      lsbz = np.asarray(lsbdata_arr[1, :]).ravel()

    N_eff = min(int(N), usbz.size, lsbz.size)
    usbz = usbz[:N_eff]
    lsbz = lsbz[:N_eff]

    ts = 1.0 / sample_freq
    freq = np.fft.fftshift(np.fft.fftfreq(N_eff, d=ts))

    usbfft = np.fft.fftshift(np.fft.fft(usbz, n=N_eff))
    lsbfft = np.fft.fftshift(np.fft.fft(lsbz, n=N_eff))

    usbpow = np.abs(usbfft) ** 2
    lsbpow = np.abs(lsbfft) ** 2

    ax.plot(freq / 1e6, usbpow, label=f"USB {usb_freq}MHz",c="cornflowerblue")
    ax.scatter(freq / 1e6, usbpow, s=5,c="cornflowerblue")
    ax.plot(freq / 1e6, lsbpow, alpha=0.3, label=f"LSB {lsb_freq}MHz",c="red")
    ax.scatter(freq / 1e6, lsbpow, s=5,c="red")

    ax.axvline(x=-sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x= sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x=0, c="black")
    ax.set_yscale("log")
    ax.legend(loc="lower left")

  else:
    data = data[1]

    # Titles
  if signal_freq2 is None and usb_freq is None:
    ax.set_title(f"Power Spectrum of {signal_freq}MHz Signal Sampled at {sample_freq/1e6}MHz")
  elif split:
    ax.set_title(f"Power Spectrum of Combined {signal_freq}MHz and {signal_freq2}Mhz Signal")
  else:
    ax.set_title(f"Power Spectrum of Mixed {signal_freq}MHz LO and {lsb_freq}/{usb_freq}Mhz RF Signals Sampled at {sample_freq/1e6}MHz")

    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("log Power (Arbitrary Units)")
    ax.grid(True)

