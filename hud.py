import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QFontDatabase, QPolygon
from PySide6.QtCore import Qt, QTimer, QPoint
from math import sin, cos, radians

class HUD(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initData()
        
    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('HUD Display')
        self.setStyleSheet("background-color: black;")
        
    def initData(self):
        self.heading = 0    # yaw (derece)
        self.pitch = 0      # pitch (derece)
        self.roll = 0       # roll (derece)
        self.altitude = 0   # metre
        self.airspeed = 0   # m/s
        self.vertical_speed = 0  # m/s
        self.armed = False
        self.gps_status = "No GPS"
        self.battery_voltage = 0
        self.battery_current = 0
        self.battery_percent = 0
        
    def drawPitchLadder(self, painter, center_x, center_y):
        # Pitch merdiveni çizimi
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        pitch_spacing = 20  # Her çizgi arası piksel
        
        for i in range(-30, 31, 10):
            y_pos = center_y + (i - self.pitch) * pitch_spacing
            line_width = 60 if i == 0 else 40
            
            # Pitch çizgileri
            painter.drawLine(center_x - line_width, y_pos   , 
                           center_x + line_width, y_pos)
            print((y_pos))
            # Pitch değerleri
            if i != 0:
                painter.drawText(center_x + line_width + 5, y_pos + 5, f"{abs(i)}°")
                painter.drawText(center_x - line_width - 25, y_pos + 5, f"{abs(i)}°")

    def drawHeadingIndicator(self, painter, center_x):
        # Üst kısımdaki yaw (heading) göstergesi
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        y_pos = 30
        width = 400
        
        # Arka plan çubuğu
        painter.drawRect(center_x - width//2, y_pos, width, 30)
        
        # Heading değerleri ve işaretler
        for i in range(-60, 61, 10):
            heading = (self.heading + i) % 360
            x_pos = center_x + i * 5
            
            if heading % 30 == 0:
                # Ana yönler
                painter.drawLine(x_pos, y_pos + 5, x_pos, y_pos + 25)
                heading_text = ""
                if heading == 0:
                    heading_text = "N"
                elif heading == 90:
                    heading_text = "E"
                elif heading == 180:
                    heading_text = "S"
                elif heading == 270:
                    heading_text = "W"
                else:
                    heading_text = str(heading)
                painter.drawText(x_pos - 10, y_pos - 5, heading_text)
            else:
                painter.drawLine(x_pos, y_pos + 10, x_pos, y_pos + 20)

        # Merkez işareti
        points = [
            QPoint(center_x, y_pos - 5),
            QPoint(center_x - 5, y_pos),
            QPoint(center_x + 5, y_pos)
        ]
        painter.drawPolygon(QPolygon(points))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        
        # Renkler
        sky_color = QColor(100, 140, 255, 180)
        ground_color = QColor(120, 180, 70, 180)
        hud_color = QColor(0, 255, 0)
        warning_color = QColor(255, 0, 0)
        
        # Font ayarları
        painter.setFont(QFont('Arial', 12))
        
        # Yapay ufuk
        horizon_offset = -self.pitch * 10  # Pitch etkisi
        painter.setPen(Qt.NoPen)
        
        # Gökyüzü
        painter.setBrush(sky_color)
        painter.drawRect(0, 0, width, center_y + horizon_offset)
        
        # Yeryüzü
        painter.setBrush(ground_color)
        painter.drawRect(0, center_y + horizon_offset, width, height)
        
        # Pitch merdiveni
        self.drawPitchLadder(painter, center_x, center_y)
        
        # Heading göstergesi
        self.drawHeadingIndicator(painter, center_x)
        
        # Merkez uçak sembolü
        painter.setPen(QPen(hud_color, 2))
        painter.drawLine(center_x - 40, center_y, center_x - 15, center_y)  # Sol kanat
        painter.drawLine(center_x + 15, center_y, center_x + 40, center_y)  # Sağ kanat
        painter.drawLine(center_x, center_y - 15, center_x, center_y + 15)  # Dikey çizgi
        painter.drawPoint(center_x, center_y)  # Merkez nokta
        
        # Sol panel - Hız göstergesi
        speed_box_width = 80
        speed_box_height = 150
        painter.drawRect(30, center_y - speed_box_height//2, speed_box_width, speed_box_height)
        painter.drawText(35, center_y - speed_box_height//2 - 20, f"SPEED")
        painter.drawText(35, center_y, f"{self.airspeed:.1f}")
        painter.drawText(35, center_y + 20, "m/s")
        
        # Sağ panel - İrtifa göstergesi
        alt_box_width = 80
        painter.drawRect(width - 110, center_y - speed_box_height//2, alt_box_width, speed_box_height)
        painter.drawText(width - 105, center_y - speed_box_height//2 - 20, f"ALT")
        painter.drawText(width - 105, center_y, f"{self.altitude:.1f}")
        painter.drawText(width - 105, center_y + 20, "m")
        
        # Üst merkez - Pitch ve Roll değerleri
        painter.drawText(center_x - 100, 80, f"PITCH: {self.pitch:.1f}°")
        painter.drawText(center_x + 20, 80, f"ROLL: {self.roll:.1f}°")
        
        # Armed/Disarmed durumu
        painter.setPen(QPen(warning_color if not self.armed else hud_color, 2))
        status_text = "ARMED" if self.armed else "DISARMED"
        painter.drawText(10, 30, status_text)
        
        # Alt bilgi satırı
        info_text = f"BAT: {self.battery_voltage:.1f}V {self.battery_current:.1f}A {self.battery_percent}% | GPS: {self.gps_status}"
        painter.setPen(QPen(hud_color, 1))
        painter.drawText(10, height - 10, info_text)

    def updateData(self, heading, pitch, roll, altitude, airspeed, vertical_speed, armed=False):
        self.heading = heading
        self.pitch = pitch
        self.roll = roll
        self.altitude = altitude
        self.airspeed = airspeed
        self.vertical_speed = vertical_speed
        self.armed = armed
        self.update()

def main():
    app = QApplication(sys.argv)
    
    hud = HUD()
    hud.show()
    
    # Test için veri güncelleme zamanlayıcısı
    timer = QTimer()
    i = 0
    
    def update():
        nonlocal i
        # Test verileri
        heading = i % 360  # 0-360 derece yaw
        pitch = sin(radians(i)) * 20  # -20 ile +20 derece arası pitch
        roll = sin(radians(i)) * 15  # -15 ile +15 derece arası roll
        altitude = 100 + sin(radians(i)) * 10  # 90-110 metre arası
        airspeed = 15 + sin(radians(i)) * 2  # 13-17 m/s arası
        vertical_speed = sin(radians(i)) * 2
        armed = i % 100 > 50
        
        hud.updateData(heading, pitch, roll, altitude, airspeed, vertical_speed, armed)
        i += 1
    
    timer.timeout.connect(update)
    timer.start(100)  # 20 FPS
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()