
"""
Kamera test kodu.

"""

import cv2

cap = cv2.VideoCapture(0) # Kamera idsi ne ise o konulmalı. Örneğin 0 yerine 1,2,3 gibi 

while True:
    _,img = cap.read()

    cv2.imshow("img",img)
    
    if cv2.waitKey(1) ==27: # ESC ile çıkma kodu 
        break

cv2.destroyAllWindows() 
cap.release()