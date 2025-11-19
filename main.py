# -----------------------------------------------------------------------------
# Main function for the driver's fatigue level estimation algorithm
# -----------------------------------------------------------------------------

import cv2
from utils import *
from detection.face import *
from detection.pose import *
from state import *
import mediapipe as mp
import time
import os
from threading import Thread
import winsound 

stop_alarm = False

def play_alarm_sound():
    global stop_alarm
    while not stop_alarm:
        try:
            winsound.Beep(2500, 500) 
        except:
            break
        
        if stop_alarm:
            break

# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------

def main():
    global stop_alarm

    # Thresholds defined for driver state evaluation
    marThresh = 0.7
    marThresh2 = 0.15
    headThresh = 6
    earThresh = 0.28
    blinkThresh = 10
    gazeThresh = 5

    # إعداد الكاميرا
    cap = cv2.VideoCapture(0)

    if (cap.isOpened() == False): 
        print("Error opening video stream or file")

    faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    captureFps = cap.get(cv2.CAP_PROP_FPS)

    driverState = DriverState(marThresh, marThresh2, headThresh, earThresh, blinkThresh, gazeThresh)
    headPose = HeadPose(faceMesh)
    faceDetector = FaceDetector(faceMesh, captureFps, marThresh, marThresh2, headThresh, earThresh, blinkThresh)

    consecutive_drowsy_frames = 0 
    alarm_thread_started = False 

    # حدد عدد الفريمات المطلوبة هنا ( 30)
    DROWSY_LIMIT = 30

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
        
        frame, results = headPose.process_image(frame)
        frame = headPose.estimate_pose(frame, results, True)
        roll, pitch, yaw = headPose.calculate_angles()

        frame, sleepEyes, mar, gaze, yawning, baseR, baseP, baseY, baseG = faceDetector.evaluate_face(frame, results, roll, pitch, yaw, True)

        frame, state = driverState.eval_state(frame, sleepEyes, mar, roll, pitch, yaw, gaze, yawning, baseR, baseP, baseG)

        # -----------------------------------------------------------
        # --- منطق العداد (30 فريم) + المكان الجديد ---
        # -----------------------------------------------------------
        
        if state == "Drowsy":
            consecutive_drowsy_frames += 1
        else:
            consecutive_drowsy_frames = 0
            stop_alarm = True
            alarm_thread_started = False 

        cv2.putText(frame, f"Frames: {consecutive_drowsy_frames}/{DROWSY_LIMIT}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        # --- (تم التعديل) الشرط أصبح 30 فريم ---
        if consecutive_drowsy_frames >= DROWSY_LIMIT:
            
            # رسالة التنبيه في وسط الشاشة
            cv2.putText(frame, "!!! WAKE UP !!!", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 5)
            
            if not alarm_thread_started:
                stop_alarm = False 
                alarm_thread_started = True
                t = Thread(target=play_alarm_sound)
                t.daemon = True
                t.start()
                print("ALARM START!!!")

        # -----------------------------------------------------------

        cv2.imshow('Driver State Monitoring', frame)

        if cv2.waitKey(10) & 0xFF == 27:
            stop_alarm = True 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()