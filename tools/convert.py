import wfdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq

# Dosya yolu (sadece dosya adı değil, klasör yolu da dahil olmalı)
record_path = '/home/bugraalp/personalFiles/embedded/STM32/STM32CubeIDE/workspace_1.14.0/ECG_Screen/patients/16265'
output_excel_file = '16265_ecg_time_trimmed_data.xlsx'

# Parametreler
start_time_seconds = 0
end_time_seconds = 10
lowcut_freq = 0.5
highcut_freq = 100
filter_order = 2

fs = 128
try:
    # Başlık dosyasını oku ve örnekleme frekansını al
    full_record_header = wfdb.rdheader(record_path)
    fs = full_record_header.fs

    start_sample = int(start_time_seconds * fs)
    end_sample = int(end_time_seconds * fs)

    # Kırpılmış kaydı oku
    record = wfdb.rdrecord(record_path, sampto=end_sample, sampfrom=start_sample)

    # Ham sinyali DataFrame'e aktar
    ecg_df = pd.DataFrame(record.p_signal, columns=record.sig_name)

    # Butterworth Bandpass filtresi tasarımı
    nyquist = 0.5 * fs
    low = lowcut_freq / nyquist
    high = highcut_freq / nyquist
    b, a = signal.butter(filter_order, [low, high], btype='bandpass')

    # Filtreleme işlemi
    filtered_signal = signal.filtfilt(b, a, record.p_signal, axis=0)
    ecg_df_filtered = pd.DataFrame(filtered_signal, columns=record.sig_name)

    # Excel'e kaydet
    ecg_df_filtered.to_excel(output_excel_file, index=False)
    print(f"✅ Filtrelenmiş veri '{output_excel_file}' dosyasına kaydedildi.")

    # Zaman ekseni
    time_vector = np.arange(ecg_df_filtered.shape[0]) / fs

    # Grafiği çiz (orijinal + filtrelenmiş)
    plt.figure(figsize=(15, 5))
    plt.plot(time_vector, ecg_df_filtered.iloc[:, 0], label='Filtrelenmiş Sinyal', color='blue')
    plt.plot(time_vector, ecg_df.iloc[:, 0], label='Orijinal Sinyal', color='red', alpha=0.5, linestyle='--')
    plt.title(f'ECG Sinyali - Kanal 1 ({record.record_name})')
    plt.xlabel('Zaman (s)')
    plt.ylabel('Amplitüd (mV)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # FFT Hesaplama
    signal_data = ecg_df_filtered.iloc[:, 0].values
    N_fft = len(signal_data)
    fft_result = fft(signal_data)
    fft_magnitude = np.abs(fft_result)[:N_fft//2] * 2 / N_fft
    fft_frequencies = fftfreq(N_fft, 1/fs)[:N_fft//2]
    dominant_idx = np.argmax(fft_magnitude)
    dominant_frequency = fft_frequencies[dominant_idx]

    # FFT Grafiği
    plt.figure(figsize=(10, 4))
    plt.plot(fft_frequencies, fft_magnitude)
    plt.title("Filtrelenmiş Sinyalin Frekans Spektrumu (FFT)")
    plt.xlabel("Frekans (Hz)")
    plt.ylabel("Genlik")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"\n❌ Bir hata oluştu: {e}")

