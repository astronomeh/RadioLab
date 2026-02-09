import numpy as np
import matplotlib.pyplot as plt
import os, re, io, zipfile


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
    ax.set_xlim(0,1e-5)
    ax.scatter(x,data,c="red",s=10)
  
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
  data = data[1]
  data = np.fft.fft(data)
  
  ts = 1.0 / sample_freq
  freq = np.fft.fftshift(np.fft.fftfreq(N, d=ts))
  mag = np.fft.fftshift(np.abs(data))
  mask = (freq >= 0) & (freq <= sample_freq/2)
  ax.plot(freq[mask]/1e6, mag[mask], c="green")
  ax.scatter(freq[mask]/1e6, mag[mask],c="red")
  ax.set_xlim(0.4,0.6)
  ax.set_xlabel("Frequency (MHz)")
  ax.set_ylabel("Voltage (Arbitrary Units)")
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
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Power (Arbitrary Units)")
    ax.axvline(x=-sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x= sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x=0, c="black")
    ax.set_yscale("log")
    ax.legend(loc="lower left")

  else:
    # --- pull real signal ---
    data = np.asarray(data[1]).ravel()

    # --- choose N_eff safely ---
    N_eff = min(int(N), data.size)
    data = data[:N_eff]

    # --- DC offset + Hann window (match your f_obs code) ---
    data0 = data - np.mean(data)
    w = np.hanning(N_eff)
    dataw = data0 * w

    # --- FFT + power ---
    ts = 1.0 / sample_freq
    freq = np.fft.fftshift(np.fft.fftfreq(N_eff, d=ts))
    datafft = np.fft.fftshift(np.fft.fft(dataw, n=N_eff))
    pow = np.abs(datafft) ** 2

    # --- peak in [0, fs/2], but if it's 0 use next highest ---
    mask = (freq >= 0) & (freq <= sample_freq/2)
    fpk_hz = _peak_from_spectrum(freq[mask], pow[mask])

    # --- plot ---
    ax.plot(freq / 1e6, pow, c="red")
    ax.scatter(freq / 1e6, pow, s=5, c="cornflowerblue")
    ax.axvline(x=-sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x= sample_freq / 2e6, c="black", ls="--")
    ax.axvline(x=0, c="black")
    ax.set_yscale("log")
    ax.set_ylim(bottom=1e-5)

    # --- label the peak frequency ---
    ax.text(0.98, 0.95, f"Peak: {fpk_hz/1e6:.3f} MHz",
            transform=ax.transAxes, ha="right", va="top")

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


def plot_fobs_vs_fs(signal_freq, sample_freq=3e6, split=False, N=4096,
                    data=None, usbdata=None, lsbdata=None,
                    signal_freq2=None, usb_freq=None, lsb_freq=None,
                    ax=None, show=False):
  """
  f_obs vs f_s (aliasing) plot.

  Pass directory path as `data=...` containing digital_sin_*.npz.
  Each npz is loaded as np.load(fp)["arr_0"].

  Conventions:
    - signal_freq in MHz
    - sample_freq in Hz
    - plot axes in MHz
  """
  if ax is None:
    fig, ax = plt.subplots()

  if usb_freq is not None:
    raise ValueError("plot_fobs_vs_fs is for real-data directory scans (usb/lsb not used).")

  if data is None or not isinstance(data, str):
    raise ValueError("Pass the DATA DIRECTORY string as `data=...`.")

  data_dir = data

  def _parse_fs_from_name(fn):
    m = re.search(r"digital_sin_([0-9]+(?:\.[0-9]+)?)", fn)
    return float(m.group(1)) if m else None

  def _load_arr0(fp):
    if fp.lower().endswith(".npz"):
      with np.load(fp, allow_pickle=True) as z:
        arr = z["arr_0"]
    else:
      arr = np.load(fp, allow_pickle=True)

    if getattr(arr, "dtype", None) == object:
      arr = np.asarray(arr.tolist(), dtype=float)
    return arr

  def _peak_freq_hz(x, fs_hz, N_use):
    x = np.asarray(x).ravel()
    N_eff = min(int(N_use), x.size)
    x = x[:N_eff]

    # DC offset removal
    x0 = x - np.mean(x)
  
    # Hann window
    w = np.hanning(N_eff)
    xw = x0 * w

    # FFT power
    V = np.fft.fft(xw)
    P = np.abs(V) ** 2
    f = np.fft.fftfreq(N_eff, d=1.0/fs_hz)

    # consider only [0, fs/2]
    mask = (f >= 0) & (f <= fs_hz/2)
    fpos = f[mask]
    Ppos = P[mask]

    # strongest bin
    k1 = int(np.argmax(Ppos))

    # if peak is at 0 Hz, use next-highest
    if fpos[k1] == 0.0:
      order = np.argsort(Ppos)[::-1]  # descending power
      for k in order:
        if fpos[k] != 0.0:
          return float(fpos[k])
      return 0.0  # fallback

    return float(fpos[k1])


  # ---- scan directory ----
  pts = []
  for fn in os.listdir(data_dir):
    if not (fn.startswith("digital_sin_") and fn.lower().endswith(".npz")):
      continue

    fs_hz = _parse_fs_from_name(fn)
    if fs_hz is None:
      continue

    fp = os.path.join(data_dir, fn)
    arr = _load_arr0(fp)

    # lab1 real-data convention: signal in arr[1] if 2D :contentReference[oaicite:0]{index=0}
    x = arr[1] if (hasattr(arr, "ndim") and arr.ndim >= 2) else arr

    fpk = _peak_freq_hz(x, fs_hz, N)
    pts.append((fs_hz, fpk))

  if len(pts) == 0:
    raise ValueError(f"No digital_sin_*.npz files found in: {data_dir}")

  pts = np.array(sorted(pts, key=lambda r: r[0]), dtype=float)
  fs_meas_hz = pts[:, 0]
  fobs_meas_hz = pts[:, 1]

  # ---- theory via mod formula ----
  f0_hz = float(signal_freq) * 1e6
  fs_min = 5e5
  fs_max = 5e6
  fs_theory_hz = np.geomspace(max(1e3, fs_min), fs_max, 1200)

  fobs_theory_hz = np.abs(((f0_hz + fs_theory_hz/2) % fs_theory_hz) - fs_theory_hz/2)

  # ---- plot in MHz ----
  fs_theory_mhz = fs_theory_hz / 1e6
  fobs_theory_mhz = fobs_theory_hz / 1e6
  fs_meas_mhz = fs_meas_hz / 1e6
  fobs_meas_mhz = fobs_meas_hz / 1e6

  ax.plot(fs_theory_mhz, fs_theory_mhz/2, "--", lw=2, alpha=0.9, label=r"$f_s/2$",c="red")
  ax.plot(fs_theory_mhz, fobs_theory_mhz, lw=2, label=r"Theory $f_{obs}$",c="green")
  ax.scatter(fs_meas_mhz, fobs_meas_mhz, s=25, c="black", label="Measured peaks", zorder=5)
  ax.axhline(1, linestyle="--", linewidth=1.5, alpha=0.8)

  # highlight closest to sample_freq argument
  i = int(np.argmin(np.abs(fs_meas_hz - float(sample_freq))))
  ax.scatter(fs_meas_mhz[i], fobs_meas_mhz[i], s=70, c="#D4AF37",
             edgecolor="black", zorder=6,
             label=f"highlight fs={sample_freq/1e6:.2f} MHz")

  ax.set_xscale("log")
  ax.set_xlim(fs_min/1e6, fs_max/1e6)
  ax.set_ylim(0,1.5)
  ax.set_xlabel("Sampling frequency $f_s$ (MHz)")
  ax.set_ylabel("Observed frequency $f_{obs}$ (MHz)")
  ax.set_title(r"$f_{obs}$ vs $f_s$ (Aliasing)")
  ax.grid(True, which="both", ls="--", alpha=0.5)
  ax.legend(loc="best")

  if show:
    plt.show()

  return fs_meas_hz, fobs_meas_hz
                      
def _peak_from_spectrum(freq, P):
  """Return peak frequency in Hz. If peak is at 0, return next-highest."""
  freq = np.asarray(freq)
  P = np.asarray(P)

  # only non-negative freqs
  mask = freq >= 0
  fpos = freq[mask]
  Ppos = P[mask]

  k1 = int(np.argmax(Ppos))
  if fpos[k1] == 0.0:
    order = np.argsort(Ppos)[::-1]
    for k in order:
      if fpos[k] != 0.0:
        return float(fpos[k])
    return 0.0
  return float(fpos[k1])

