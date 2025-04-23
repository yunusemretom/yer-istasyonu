"""
Ana koddur bu. Aruco okuma ve buna göre aracın tepki verme kodudur.

Created by Yunus Emre TOM

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


#master = mavutil.mavlink_connection('udpin:localhost:14551')

print("Baglanti bekleniyor...")  
master.wait_heartbeat()
print("Baglanti onaylandi.") 


def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(9)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

def hizalanma(x,y):
    deger_y = 1500-((cap_w_center-x)//5)
    deger_x = 1500-((cap_h_center-y)//5)
    set_rc_channel_pwm(1,deger_y)
    set_rc_channel_pwm(2,deger_x)

ARUCO_DICT = {
	#"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	#"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	#"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	#"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	#"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	#"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	#"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	#"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}
# Burada hangi idleri kullanmak istiyorsanız onun yorum satırını açarabilirsiniz 


def detect_markers(image):
    
    aruco_type_list = []
    
    for aruco_type, dictionary_id in ARUCO_DICT.items():

        arucoDict = cv2.aruco.getPredefinedDictionary(dictionary_id)
        arucoParams = cv2.aruco.DetectorParameters()

        corners, ids, _ = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

        if len(corners) > 0:
            
            aruco_type_list.append(aruco_type)
            
            print(f"Markers detected using {aruco_type} dictionary")

            for markerCorner, markerId in zip(corners, ids.flatten()):
                corners_aruco = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners_aruco

                cv2.polylines(image, [markerCorner.astype(int)], True, (0, 255, 0), 2)

                cX = int((topLeft[0] + bottomRight[0]) / 2)
                cY = int((topLeft[1] + bottomRight[1]) / 2)
                hizalanma(cX,cY) #hizzalama için gerekli değerleri veriyor

                cv2.circle(image, (cX, cY), 5, (255, 0, 0), -1)
                cv2.putText(image, str(aruco_type) + " " + str(int(markerId)),
                            (int(topLeft[0] - 5), int(topLeft[1])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))

            # break  # Stop iterating once markers are detected        
        # cv2.imshow("Detected Markers", image)
            
    return aruco_type_list

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters()

    corners, ids, rejected = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    
    if len(corners) > 0:
        for i in range(0, len(ids)):
            
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.025, matrix_coefficients, distortion_coefficients)
            
            #x = int((corners[i][0][2][0]+corners[i][0][0][0])//2)
            #y = int((corners[i][0][2][1]+corners[i][0][0][1])//2)

            #hizalanma(x,y) # hizzlanma kodu görüntüde bulduğu değere göre hızlanma yapıyor.

            cv2.aruco.drawDetectedMarkers(frame, corners) 
            #cv2.circle(image, (x,y),10,(0, 0, 200), 5)
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01) 
             
    return frame


if __name__ == "__main__":

    image_path = r"arucoMarkers/singlemarkersoriginal.jpg"

    intrinsic_camera = np.array(((933.15867, 0, 657.59), (0, 933.1586, 400.36993), (0, 0, 1)))
    distortion = np.array((-0.43948, 0.18514, 0, 0))

    cap = cv2.VideoCapture(1)
    
    cap_w_center = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2)
    cap_h_center = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2)
    
    while cap.isOpened():

        message = master.recv_match(type='RC_CHANNELS', blocking=True).to_dict() #8. kanalı almak ve sürekli kontrol etme kodu
        kanal_8_deger=message["chan8_raw"]
        print(kanal_8_deger)

        message = master.recv_match(type='SYS_STATUS', blocking=True) # syste değerlerini alıyor
        fail_safe_status = message.onboard_control_sensors_present & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_RC_RECEIVER #failsafe kontrolu

        if fail_safe_status == 0:
            print("Kumanda bağlı değil!!!")
            continue

        elif fail_safe_status != 0 and kanal_8_deger < 1500:
            print("kontrol pixhawkta")
            continue
        
        else:
            ret, image = cap.read()

            for aruco_type in detect_markers(image):
                image = pose_estimation(image, ARUCO_DICT[aruco_type], intrinsic_camera, distortion)
                
            cv2.imshow('Estimated Pose', image)
                    
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


"""
Ana koddur bu. Aruco okuma ve buna göre aracın tepki verme kodudur.

Created by Yunus Emre TOM

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


#master = mavutil.mavlink_connection('udpin:localhost:14551')

print("Baglanti bekleniyor...")  
master.wait_heartbeat()
print("Baglanti onaylandi.") 


def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(9)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

def hizalanma(x,y):
    deger_y = 1500-((cap_w_center-x)//5)
    deger_x = 1500-((cap_h_center-y)//5)
    set_rc_channel_pwm(1,deger_y)
    set_rc_channel_pwm(2,deger_x)

ARUCO_DICT = {
	#"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	#"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	#"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	#"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	#"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	#"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	#"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	#"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}
# Burada hangi idleri kullanmak istiyorsanız onun yorum satırını açarabilirsiniz 


def detect_markers(image):
    
    aruco_type_list = []
    
    for aruco_type, dictionary_id in ARUCO_DICT.items():

        arucoDict = cv2.aruco.getPredefinedDictionary(dictionary_id)
        arucoParams = cv2.aruco.DetectorParameters()

        corners, ids, _ = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

        if len(corners) > 0:
            
            aruco_type_list.append(aruco_type)
            
            print(f"Markers detected using {aruco_type} dictionary")

            for markerCorner, markerId in zip(corners, ids.flatten()):
                corners_aruco = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners_aruco

                cv2.polylines(image, [markerCorner.astype(int)], True, (0, 255, 0), 2)

                cX = int((topLeft[0] + bottomRight[0]) / 2)
                cY = int((topLeft[1] + bottomRight[1]) / 2)
                hizalanma(cX,cY) #hizzalama için gerekli değerleri veriyor

                cv2.circle(image, (cX, cY), 5, (255, 0, 0), -1)
                cv2.putText(image, str(aruco_type) + " " + str(int(markerId)),
                            (int(topLeft[0] - 5), int(topLeft[1])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))

            # break  # Stop iterating once markers are detected        
        # cv2.imshow("Detected Markers", image)
            
    return aruco_type_list

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters()

    corners, ids, rejected = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    
    if len(corners) > 0:
        for i in range(0, len(ids)):
            
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.025, matrix_coefficients, distortion_coefficients)
            
            #x = int((corners[i][0][2][0]+corners[i][0][0][0])//2)
            #y = int((corners[i][0][2][1]+corners[i][0][0][1])//2)

            #hizalanma(x,y) # hizzlanma kodu görüntüde bulduğu değere göre hızlanma yapıyor.

            cv2.aruco.drawDetectedMarkers(frame, corners) 
            #cv2.circle(image, (x,y),10,(0, 0, 200), 5)
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01) 
             
    return frame


if __name__ == "__main__":

    image_path = r"arucoMarkers/singlemarkersoriginal.jpg"

    intrinsic_camera = np.array(((933.15867, 0, 657.59), (0, 933.1586, 400.36993), (0, 0, 1)))
    distortion = np.array((-0.43948, 0.18514, 0, 0))

    cap = cv2.VideoCapture(1)
    
    cap_w_center = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2)
    cap_h_center = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2)
    
    while cap.isOpened():

        message = master.recv_match(type='RC_CHANNELS', blocking=True).to_dict() #8. kanalı almak ve sürekli kontrol etme kodu
        kanal_8_deger=message["chan8_raw"]
        print(kanal_8_deger)

        message = master.recv_match(type='SYS_STATUS', blocking=True) # syste değerlerini alıyor
        fail_safe_status = message.onboard_control_sensors_present & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_RC_RECEIVER #failsafe kontrolu

        if fail_safe_status == 0:
            print("Kumanda bağlı değil!!!")
            continue

        elif fail_safe_status != 0 and kanal_8_deger < 1500:
            print("kontrol pixhawkta")
            continue
        
        else:
            ret, image = cap.read()

            for aruco_type in detect_markers(image):
                image = pose_estimation(image, ARUCO_DICT[aruco_type], intrinsic_camera, distortion)
                
            cv2.imshow('Estimated Pose', image)
                    
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

