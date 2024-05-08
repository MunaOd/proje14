import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog

class IsTakipSistemi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('İş Takip ve Yönetim Sistemi')
        self.setGeometry(100, 100, 300, 250)
        self.layout = QVBoxLayout()

        # Proje oluşturma 
        self.proje_adi_label = QLabel('Proje Adı:')
        self.proje_adi_input = QLineEdit()
        self.baslangic_label = QLabel('Başlangıç Tarihi:')
        self.baslangic_input = QLineEdit()
        self.bitis_label = QLabel('Bitiş Tarihi:')
        self.bitis_input = QLineEdit()
        self.proje_olustur_button = QPushButton('Proje Oluştur')
        self.proje_olustur_button.clicked.connect(self.proje_olustur)

        self.layout.addWidget(self.proje_adi_label)
        self.layout.addWidget(self.proje_adi_input)
        self.layout.addWidget(self.baslangic_label)
        self.layout.addWidget(self.baslangic_input)
        self.layout.addWidget(self.bitis_label)
        self.layout.addWidget(self.bitis_input)
        self.layout.addWidget(self.proje_olustur_button)

        # Çalışan oluşturma 
        self.calisan_adi_label = QLabel('Çalışanın Adı:')
        self.calisan_adi_input = QLineEdit()
        self.calisan_departman_label = QLabel('Departman:')
        self.calisan_departman_input = QLineEdit()
        self.calisan_olustur_button = QPushButton('Çalışan Oluştur')
        self.calisan_olustur_button.clicked.connect(self.calisan_olustur)

        self.layout.addWidget(self.calisan_adi_label)
        self.layout.addWidget(self.calisan_adi_input)
        self.layout.addWidget(self.calisan_departman_label)
        self.layout.addWidget(self.calisan_departman_input)
        self.layout.addWidget(self.calisan_olustur_button)

        # Görev oluşturma 
        self.gorev_adi_label = QLabel('Görev Adı:')
        self.gorev_adi_input = QLineEdit()
        self.sorumlu_kisi_label = QLabel('Sorumlu Kişi:')
        self.sorumlu_kisi_input = QLineEdit()
        self.ilerleme_label = QLabel('İlerleme (%):')
        self.ilerleme_input = QLineEdit()
        self.gorev_olustur_button = QPushButton('Görev Oluştur')
        self.gorev_olustur_button.clicked.connect(self.gorev_olustur)

        self.layout.addWidget(self.gorev_adi_label)
        self.layout.addWidget(self.gorev_adi_input)
        self.layout.addWidget(self.sorumlu_kisi_label)
        self.layout.addWidget(self.sorumlu_kisi_input)
        self.layout.addWidget(self.ilerleme_label)
        self.layout.addWidget(self.ilerleme_input)
        self.layout.addWidget(self.gorev_olustur_button)

        self.rapor_olustur_button = QPushButton('Rapor Oluştur')
        self.rapor_olustur_button.clicked.connect(self.goster_log)
        self.layout.addWidget(self.rapor_olustur_button)


        self.setLayout(self.layout)
        self.show()

        # Veritabanı bağlantısı
        self.baglanti_olustur()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect('is_takip.db')
        self.cursor = self.baglanti.cursor()
        self.cursor.execute('''DROP TABLE IF EXISTS projeler''')#delete after first run
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS projeler (
                                proje_id INTEGER PRIMARY KEY,
                                proje_adi TEXT,
                                baslangic_tarihi DATE,
                                bitis_tarihi DATE)''')
        self.cursor.execute('''DROP TABLE IF EXISTS calisanlar''')#delete after first run
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS calisanlar (
                                calisan_id INTEGER PRIMARY KEY,
                                calisan_adi TEXT,
                                departman TEXT)''')
        self.cursor.execute('''DROP TABLE IF EXISTS gorevler''')#delete after first run
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS gorevler (
                                gorev_id INTEGER PRIMARY KEY,
                                gorev_adi TEXT,
                                sorumlu_kisi TEXT,
                                ilerleme INTEGER)''')
        self.cursor.execute('''DROP TABLE IF EXISTS creation_log''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS creation_log (
                                id INTEGER PRIMARY KEY,
                                log TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')  # Corrected SQL command
        self.baglanti.commit()

    def proje_olustur(self):
        proje_adi = self.proje_adi_input.text()
        baslangic_tarihi = self.baslangic_input.text()
        bitis_tarihi = self.bitis_input.text()

        self.cursor.execute("INSERT INTO projeler (proje_adi, baslangic_tarihi, bitis_tarihi) VALUES (?, ?, ?)",
                            (proje_adi, baslangic_tarihi, bitis_tarihi))
        self.baglanti.commit()
        self.proje_adi_input.clear()
        self.baslangic_input.clear()
        self.bitis_input.clear()

        self.log_creation(f"Proje oluşturuldu: Proje Adı: {proje_adi}, Başlangıç Tarihi: {baslangic_tarihi}, Bitiş Tarihi: {bitis_tarihi}")

    def calisan_olustur(self):
        calisan_adi = self.calisan_adi_input.text()
        departman = self.calisan_departman_input.text()

        self.cursor.execute("INSERT INTO calisanlar (calisan_adi, departman) VALUES (?, ?)", (calisan_adi, departman))
        self.baglanti.commit()
        self.calisan_adi_input.clear()
        self.calisan_departman_input.clear()

        self.log_creation(f"Çalışan oluşturuldu: Çalışan Adı: {calisan_adi}, Departman: {departman}")

    def gorev_olustur(self):
        gorev_adi = self.gorev_adi_input.text()
        sorumlu_kisi = self.sorumlu_kisi_input.text()
        ilerleme = int(self.ilerleme_input.text())

        self.cursor.execute("INSERT INTO gorevler (gorev_adi, sorumlu_kisi, ilerleme) VALUES (?, ?, ?)",
                            (gorev_adi, sorumlu_kisi, ilerleme))
        self.baglanti.commit()
        self.gorev_adi_input.clear()
        self.sorumlu_kisi_input.clear()
        self.ilerleme_input.clear()

        self.log_creation(f"Görev oluşturuldu: Görev Adı: {gorev_adi}, Sorumlu Kişi: {sorumlu_kisi}, İlerleme: {ilerleme}%")

    def log_creation(self, log_text):
        self.cursor.execute("INSERT INTO creation_log (log) VALUES (?)", (log_text,))
        self.baglanti.commit()

    def goster_log(self):
        log_dialog = QDialog(self)
        log_dialog.setWindowTitle('Oluşturma Logları')
        log_layout = QVBoxLayout()

        log_text = QLabel()
        self.cursor.execute("SELECT log FROM creation_log")
        logs = self.cursor.fetchall()
        log_text.setText('\n'.join([log[0] for log in logs]))

        log_layout.addWidget(log_text)
        log_dialog.setLayout(log_layout)
        log_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = IsTakipSistemi()
    sys.exit(app.exec_())
