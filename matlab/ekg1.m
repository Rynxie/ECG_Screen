% Veriyi oku
data = readmatrix('/home/bugraalp/personalFiles/embedded/STM32/STM32CubeIDE/workspace_1.14.0/ECG_Screen-1/tools/16265_ecg_time_trimmed_data.xlsx');
ecg = data(:, 1);      % EKG sinyali (tek kanal)
fs = 128;              % Örnekleme frekansı (Hz)
t = (0:length(ecg)-1) / fs;

% Filtreleme (0.5–40 Hz bandpass)
[b, a] = butter(2, [0.5 40]/(fs/2), 'bandpass');
filtered = filtfilt(b, a, ecg);

% R peak'leri tespit et
[~, locs_R] = findpeaks(filtered, 'MinPeakHeight', 0.5, 'MinPeakDistance', round(0.3*fs));

% R-R aralıkları ve BPM
RR_intervals = diff(locs_R) / fs;
bpm = 60 ./ RR_intervals;
mean_bpm = mean(bpm);
fprintf('Ortalama BPM: %.2f\n', mean_bpm);

% Noktaları tutacak diziler
Q_points = []; S_points = [];
P_points = []; T_points = [];
QT_intervals = [];

for i = 1:length(locs_R)
    idx = locs_R(i);

    % Q ve S noktası aralığı
    left_idx = max(idx - round(0.1*fs), 1);
    right_idx = min(idx + round(0.1*fs), length(filtered));
    window_signal = filtered(left_idx:right_idx);
    len = length(window_signal);
    
    [~, q_rel] = min(window_signal(1:floor(len/2)));
    [~, s_rel] = min(window_signal(floor(len/2):end));
    
    q_idx = left_idx + q_rel - 1;
    s_idx = left_idx + floor(len/2) + s_rel - 2;
    
    Q_points(end+1) = q_idx;
    S_points(end+1) = s_idx;
    QT_intervals(end+1) = (s_idx - q_idx) / fs;

    % P noktası (R'den önce 0.2s aralık)
    p_search_start = max(idx - round(0.25*fs), 1);
    p_search_end = max(idx - round(0.1*fs), 1);
    [~, p_rel] = max(filtered(p_search_start:p_search_end));
    P_points(end+1) = p_search_start + p_rel - 1;

    % T noktası (S'den sonra 0.2–0.4s aralığı)
    t_search_start = min(s_idx + round(0.1*fs), length(filtered));
    t_search_end = min(s_idx + round(0.4*fs), length(filtered));
    [~, t_rel] = max(filtered(t_search_start:t_search_end));
    T_points(end+1) = t_search_start + t_rel - 1;
end

mean_qrs_duration = mean(QT_intervals);
fprintf('Ortalama QRS Süresi: %.3f s\n', mean_qrs_duration);

% Grafiği çiz
figure;
plot(t, filtered);
hold on;
plot(t(locs_R), filtered(locs_R), 'ro', 'DisplayName', 'R-peaks');
plot(t(Q_points), filtered(Q_points), 'go', 'DisplayName', 'Q');
plot(t(S_points), filtered(S_points), 'mo', 'DisplayName', 'S');
plot(t(P_points), filtered(P_points), 'ko', 'DisplayName', 'P');
plot(t(T_points), filtered(T_points), 'co', 'DisplayName', 'T');
legend;
xlabel('Zaman (s)');
ylabel('Genlik');
title('EKG Sinyali ve P-Q-R-S-T Noktaları');
grid on;
