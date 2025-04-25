import cv2
import numpy as np
import math

# Bu fonksiyon yapay horizon overlay çizer
def draw_attitude_overlay(frame, pitch, roll):
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)

    # Boş overlay oluştur
    overlay = np.zeros_like(frame)

    # Horizon çizgisi için temel parametreler
    pitch_offset = int(pitch * 5)  # Her derece için 5px kaydırma
    roll_rad = math.radians(roll)

    # İki nokta belirleyip döndürerek horizon çizgisi oluştur
    length = w
    x1, y1 = center[0] - length, center[1] + pitch_offset
    x2, y2 = center[0] + length, center[1] + pitch_offset

    # Dönüş matrisi uygula
    cos_r = math.cos(roll_rad)
    sin_r = math.sin(roll_rad)

    def rotate_point(x, y):
        x -= center[0]
        y -= center[1]
        xr = x * cos_r - y * sin_r
        yr = x * sin_r + y * cos_r
        return int(xr + center[0]), int(yr + center[1])

    p1 = rotate_point(x1, y1)
    p2 = rotate_point(x2, y2)

    # Horizon çizgisini overlay'e çiz
    cv2.line(overlay, p1, p2, (0, 255, 0), 2)

    # Overlay'i orijinal görüntüyle birleştir
    return cv2.addWeighted(frame, 1, overlay, 1, 0)

# Test verileri (dilersen drone verisiyle değiştirirsin)
pitch = 0
roll = 0

# Kamera başlat
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Örnek olarak sürekli artan pitch/roll simülasyonu
    pitch = (pitch + 0.5) % 360
    roll = (roll + 0.5) % 360

    # Overlay uygulama
    overlayed = draw_attitude_overlay(frame, pitch - 18, roll - 18)

    # Göster
    cv2.imshow("Flight Display", overlayed)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
