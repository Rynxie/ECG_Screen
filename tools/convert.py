import wfdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import scipy.signal as signal # Filtreleme için scipy.signal modülünü import ediyoruz

# --- AYARLANACAK KISIMLAR ---

record_path = '/home/bugraalp/personalFiles/embedded/STM32/STM32CubeIDE/workspace_1.14.0/ECG_Screen/patients/16265' 

output_excel_file = '16265_ecg_time_trimmed_data.xlsx'

start_time_seconds = 0   
end_time_seconds = 10   

# --- FİLTRELEME AYARLARI ---
# EKG sinyali için tipik frekans aralığı
lowcut_freq = 0.5  # Hz - Düşük kesim frekansı (baseline wander'ı gidermek için)
highcut_freq = 40  # Hz - Yüksek kesim frekansı (kas veya güç hattı parazitlerini gidermek için)
filter_order = 4   # Filtrenin derecesi (genellikle 2-5 arasında seçilir, daha yüksek değerler daha keskin filtreleme sağlar)
# --- FİLTRELEME AYARLARI SONU ---

# --- AYARLANACAK KISIMLAR SONU ---

try:
    full_record_header = wfdb.rdheader(record_path)
    fs = full_record_header.fs 

    start_sample = int(start_time_seconds * fs)
    end_sample = int(end_time_seconds * fs)
    
    record = wfdb.rdrecord(record_path, sampto=end_sample, sampfrom=start_sample)
    
    ecg_df = pd.DataFrame(record.p_signal, columns=record.sig_name)

    print(f"Kayıt Adı: {record.record_name}")
    print(f"Örnekleme Frekansı (Hz): {fs}")
    print(f"Orijinal Kayıt Toplam Numune Sayısı: {full_record_header.sig_len}")
    print(f"Kırpılmış Sinyal Boyutu (numune): {ecg_df.shape[0]}")
    print(f"Kırpılmış Sinyal Süresi (saniye): {ecg_df.shape[0] / fs:.2f} saniye")
    print(f"Sinyal Kanal Adları: {ecg_df.columns.tolist()}")

    # --- YENİ EKLENEN KISIM: BAND-PASS FİLTRELEME ---
    print(f"Sinyale {lowcut_freq}-{highcut_freq} Hz band-pass filtre uygulanıyor...")
    
    # Butterworth filtresi için frekansları normalize etme
    # Normalleştirilmiş frekans = 2 * (istenen_frekans / örnekleme_frekansı)
    nyquist = 0.5 * fs # Nyquist frekansı, örnekleme frekansının yarısıdır.
    low = lowcut_freq / nyquist
    high = highcut_freq / nyquist

    # Filtre katsayılarını (b ve a) tasarla
    # b: pay (numerator) katsayıları, a: payda (denominator) katsayıları
    # 'bandpass' tipi, 'butter' (Butterworth) filtresi, 'filter_order' derecesi
    b, a = signal.butter(filter_order, [low, high], btype='bandpass')

    # Filtreleme işlemini uygula
    # filtfilt fonksiyonu, sinyali hem ileri hem de geri yönde filtreleyerek faz kaymasını önler.
    # record.p_signal, WFDB'den okunan ham sinyal verisidir.
    # Bu işlem sonucunda, p_signal'daki tüm kanallar filtrelenir.
    filtered_signal = signal.filtfilt(b, a, record.p_signal, axis=0) # axis=0, sütunlar üzerinde filtreleme yapar

    # Filtrelenmiş sinyali yeni bir DataFrame'e dönüştür
    # Excel'e kaydedilecek olan bu filtrelenmiş veridir.
    ecg_df_filtered = pd.DataFrame(filtered_signal, columns=record.sig_name)
    print("Filtreleme tamamlandı.")

    # Excel çıktısı oluşturma (Şimdi filtrelenmiş veriyi kaydediyoruz)
    # output_excel_file değişkenini değiştirmedik, sadece içeriği filtrelenmiş oldu.
    ecg_df_filtered.to_excel(output_excel_file, index=False)

    print(f"Filtrelenmiş ECG sinyal verileri başarıyla '{output_excel_file}' dosyasına kaydedildi.")

    # --- İsteğe Bağlı: Kırpılmış VE FİLTRELENMİŞ Sinyali Çizme ---
    plt.figure(figsize=(15, 5))
    time_vector = np.arange(ecg_df_filtered.shape[0]) / fs
    
    # Filtrelenmiş ilk kanalı çiz
    plt.plot(time_vector, ecg_df_filtered.iloc[:, 0], label='Filtrelenmiş Sinyal (Kanal 1)', color='blue') 
    
    # İsteğe bağlı: Orijinal sinyali de arkada soluk bir şekilde çizerek farkı gösterme
    plt.plot(time_vector, ecg_df.iloc[:, 0], label='Orijinal Sinyal (Kanal 1)', color='red', alpha=0.5, linestyle='--')
    
    plt.title(f'Filtrelenmiş ECG Sinyali - Kanal 1 ({record.record_name})')
    plt.xlabel('Zaman (s)')
    plt.ylabel('Amplitüd (mV)')
    plt.grid(True)
    plt.legend() # Çizilen sinyallerin etiketlerini gösterir
    plt.show()

except Exception as e:
    print(f"\nBir hata oluştu: {e}")
    print(f"Hata detayı: {e}")
