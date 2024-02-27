
"""
Bu kod bağlantıyı deneme için autopilot verilerini çeken bir kod.

"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pymavlink import mavutil
import time


try:
    master = mavutil.mavlink_connection("/dev/ttyACM0", baud=57600) # Bağlantı portu burada yazılmalı

except:
    master = mavutil.mavlink_connection("/dev/ttyACM1", baud=57600) # Bazen bağlantı kopup yeniden geldiği zaman diğer porta geçiş yapabiliyor. Bunun için yedek port.


print("Baglanti bekleniyor...") 

master.wait_heartbeat()

print("Baglanti onaylandı.")


while True:
    try:
        print(master.recv_match().to_dict())# Verilerin geldiği ve yazdırıldığı kod
    
    except:
        pass
    
    time.sleep(0.1)