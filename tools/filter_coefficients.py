import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.signal import lfilter, firwin

#sample rate
fs = 250
df = pd.read_excel("/home/bugraalp/Downloads/ecg.ods", engine="odf")
ecg_data = df.iloc[:, 0].dropna().to_numpy()

coeffs = firwin(numtaps=32, cutoff=[0.5, 40], pass_zero=False, fs=fs)

filtered_ecg = lfilter(coeffs, 1.0, ecg_data)
print(coeffs)
plt.figure(figsize=(14, 6))
plt.plot(ecg_data, label="Original ECG signal", alpha=0.5)
plt.plot(filtered_ecg, label="Filtered ECG", linewidth=2)
plt.title("ECG Signal from Column A")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
