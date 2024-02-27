"""
Aruco için bir deneme kodu.
Created by Yunus Emre TOM
"""

import cv2
import numpy as np
import time

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
def hizalanma(x,y):
    deger_y = 1500-((cap_w_center-x)//5)
    deger_x = 1500-((cap_h_center-y)//5)
    print(deger_x)
    print(deger_y)
    print()

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
                #hizalanma(cX,cY) #hizzalama için gerekli değerleri veriyor

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
            
            x = int((corners[i][0][2][0]+corners[i][0][0][0])//2)
            y = int((corners[i][0][2][1]+corners[i][0][0][1])//2)
            hizalanma(x,y)
            
            cv2.aruco.drawDetectedMarkers(frame, corners) 
            #cv2.circle(image, (x,y),3,(0, 0, 200), 5)
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01) 
             
    return frame


if __name__ == "__main__":
    prev_frame_time = 0
  
    
    new_frame_time = 0

    image_path = r"arucoMarkers/singlemarkersoriginal.jpg"

    intrinsic_camera = np.array(((933.15867, 0, 657.59), (0, 933.1586, 400.36993), (0, 0, 1)))
    distortion = np.array((-0.43948, 0.18514, 0, 0))

    cap = cv2.VideoCapture(0)

    cap_w_center = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2)
    cap_h_center = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2)
    
    while cap.isOpened():
        ret, image = cap.read()
        new_frame_time = time.time() 
        
        cv2.circle(image, (cap_w_center,cap_h_center),3,(0, 0, 200), 5)
        for aruco_type in detect_markers(image):
             image = pose_estimation(image, ARUCO_DICT[aruco_type], intrinsic_camera, distortion)

        fps = int(1/(new_frame_time-prev_frame_time)) # Fps gösterme yeri
        prev_frame_time = new_frame_time  
        fps = str(fps)     

        cv2.putText(image, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)         
        cv2.imshow('Estimated Pose', image)
             
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()