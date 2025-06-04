import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import serial
import serial.tools.list_ports
import threading
import time
import pandas as pd
import numpy as np

class SerialCSVSender(Gtk.Window):
    def __init__(self):
        super().__init__(title="Seri Port CSV Gönderici")
        self.set_border_width(10)
        self.set_default_size(600, 300)

        self.csv_data = None
        self.serial_port = None
        self.running = False

        # Ana kutu
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Üst Grid layout
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        vbox.pack_start(grid, False, False, 0)

        # Seri port combobox
        self.combo_serial = Gtk.ComboBoxText()
        self.update_serial_ports()
        grid.attach(Gtk.Label(label="Seri Port:"), 0, 0, 1, 1)
        grid.attach(self.combo_serial, 1, 0, 1, 1)

        # CSV dosyası seçici
        self.btn_csv = Gtk.Button(label="CSV Seç")
        self.btn_csv.connect("clicked", self.on_csv_choose)
        grid.attach(self.btn_csv, 2, 0, 1, 1)

        self.label_csv = Gtk.Label(label="Seçilmedi")
        grid.attach(self.label_csv, 3, 0, 2, 1)

        # Baudrate girişi
        grid.attach(Gtk.Label(label="Baudrate:"), 0, 1, 1, 1)
        self.entry_baud = Gtk.Entry()
        self.entry_baud.set_text("9600")
        grid.attach(self.entry_baud, 1, 1, 1, 1)

        # Sütun numarası girişi
        grid.attach(Gtk.Label(label="Sütun No (0'dan başlar):"), 2, 1, 1, 1)
        self.entry_column = Gtk.Entry()
        self.entry_column.set_text("0")
        grid.attach(self.entry_column, 3, 1, 1, 1)

        # Örnekleme süresi (sample rate) girişi
        grid.attach(Gtk.Label(label="Sample Rate (ms):"), 0, 2, 1, 1)
        self.entry_sample = Gtk.Entry()
        self.entry_sample.set_text("1000")
        grid.attach(self.entry_sample, 1, 2, 1, 1)

        # Bağlan butonu
        self.btn_connect = Gtk.Button(label="Bağlan ve Gönder")
        self.btn_connect.connect("clicked", self.on_connect)
        grid.attach(self.btn_connect, 2, 2, 2, 1)

        # Konsol (TextView)
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(100)
        scrolled_window.add(self.textview)
        vbox.pack_start(scrolled_window, True, True, 0)

    def update_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.combo_serial.append_text(port.device)
        if ports:
            self.combo_serial.set_active(0)

    def on_csv_choose(self, button):
        dialog = Gtk.FileChooserDialog(
            title="CSV Dosyası Seç",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV Files")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.csv_path = dialog.get_filename()
            self.label_csv.set_text(self.csv_path)
            try:
                self.csv_data = pd.read_csv(self.csv_path)
            except Exception as e:
                self.label_csv.set_text("CSV okunamadı")
                print("CSV Hatası:", e)
        dialog.destroy()

    def append_to_console(self, text):
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, text + "\n")
        mark = self.textbuffer.create_mark(None, self.textbuffer.get_end_iter(), True)
        self.textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def on_connect(self, button):
        if self.running:
            self.running = False
            self.btn_connect.set_label("Bağlan ve Gönder")
            if self.serial_port:
                self.serial_port.close()
            return

        port = self.combo_serial.get_active_text()
        if not port or self.csv_data is None:
            self.append_to_console("Seri port veya CSV dosyası eksik.")
            return

        try:
            baud = int(self.entry_baud.get_text())
            column = int(self.entry_column.get_text())
            sample_rate = int(self.entry_sample.get_text()) / 1000.0
        except ValueError:
            self.append_to_console("Geçersiz giriş.")
            return

        try:
            self.serial_port = serial.Serial(port, baudrate=baud)
        except Exception as e:
            self.append_to_console(f"Seri port açılamadı: {e}")
            return

        self.running = True
        self.btn_connect.set_label("Durdur")

        def send_loop():
            # CSV verilerini temizle ve geçerli verileri al
            valid_data = []
            for index, row in self.csv_data.iterrows():
                try:
                    value = row[column]
                    # NaN kontrolü
                    if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
                        continue
                    # Boş string kontrolü
                    if str(value).strip() == '':
                        continue
                    valid_data.append(str(value))
                except (KeyError, IndexError):
                    continue
            
            if not valid_data:
                GLib.idle_add(self.append_to_console, "Geçerli veri bulunamadı!")
                self.running = False
                GLib.idle_add(self.btn_connect.set_label, "Bağlan ve Gönder")
                return
            
            GLib.idle_add(self.append_to_console, f"Toplam {len(valid_data)} geçerli veri bulundu. Döngülü gönderim başlıyor...")
            
            data_index = 0
            cycle_count = 1
            
            while self.running:
                try:
                    value = valid_data[data_index]
                    self.serial_port.write((value + '\r\n').encode())
                    GLib.idle_add(self.append_to_console, f"Döngü {cycle_count} - Gönderildi: {value}")
                    
                    data_index += 1
                    
                    # Veri listesinin sonuna geldiğimizde başa dön
                    if data_index >= len(valid_data):
                        data_index = 0
                        cycle_count += 1
                        GLib.idle_add(self.append_to_console, f"--- Döngü {cycle_count} başlıyor ---")
                    
                except Exception as e:
                    GLib.idle_add(self.append_to_console, f"Hata: {e}")
                    break
                    
                time.sleep(sample_rate)
            
            if self.serial_port:
                self.serial_port.close()
            self.running = False
            GLib.idle_add(self.btn_connect.set_label, "Bağlan ve Gönder")

        threading.Thread(target=send_loop, daemon=True).start()

def main():
    app = SerialCSVSender()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()