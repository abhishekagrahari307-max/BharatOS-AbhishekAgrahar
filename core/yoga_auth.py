import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    return angle

def yoga_authenticate(pose="surya_namaskar", confidence=0.85):
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=confidence) as pose_detector:
        auth_success = False
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
                
            # Process image
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose_detector.process(image)
            
            # Draw pose landmarks
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.pose_landmarks:
                # Pose detection logic
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates for key points
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
                       landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                
                # Calculate angle
                angle = calculate_angle(shoulder, hip, knee)
                
                # Authentication logic
                if 85 < angle < 95:  # Ideal right angle
                    cv2.putText(image, "Authenticated!", (50, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    auth_success = True
                else:
                    cv2.putText(image, f"Adjust Pose: {int(angle)}°", (50, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow('Yoga Authentication', image)
            if cv2.waitKey(5) & 0xFF == 27 or auth_success:
                break
                
    cap.release()
    cv2.destroyAllWindows()
    return auth_success
