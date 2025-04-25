import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from math import sin, radians

from arayuz import QPrimaryFlightDisplay  # Bu, dışardan import ettiğin PFD gösterge sınıfı

# Uygulama oluştur
app = QApplication(sys.argv)

# Göstergeleri içeren pencereyi oluştur
pfd = QPrimaryFlightDisplay()
pfd.zoom = 1  # DPI ayarı gibi düşünebilirsin
pfd.show()

# Sayaç: Telemetri verisini temsil eder
i = 0

# Update fonksiyonu (her timer tick'inde bir kez çağrılır)
def update():
    global i
    # Daha gerçekçi pitch hareketi için sinüs fonksiyonu kullanıyoruz
    pfd.roll = sin(radians(i)) * 0.2  # Roll açısını -10 ile +10 derece arasında değiştir
    pfd.pitch = sin(radians(i)) * 0.2  # Pitch açısını -20 ile +20 derece arasında değiştir
    pfd.heading = i % 360
    pfd.airspeed = 120 + sin(radians(i)) * 10  # 110-130 knot arası
    pfd.alt = 1000 + sin(radians(i)) * 100  # 900-1100 feet arası
    pfd.vspeed = sin(radians(i)) * 10  # -10 ile +10 feet/min arası
    pfd.skipskid = sin(radians(i)) * 0.5  # Slip/skid göstergesi
    pfd.update()

    i += 1
    if i > 1000:  # test için sınırlı tutabilirsin
        i = 0

# Timer kur
timer = QTimer()
timer.timeout.connect(update)
timer.start(1000 / 10)  # 60 FPS (yaklaşık 16ms)

# Uygulamayı başlat
sys.exit(app.exec())
