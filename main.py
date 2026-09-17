import cv2
from src.camera import CameraStream
from src.landmarks import FaceLandmarkExtractor
from src.metrics import compute_ear, compute_mar, compute_head_pose
from src.evaluator import StateEvaluator
from src.logger import IncidentLogger
from src.alerter import AudioAlerter
from src.config import FRAME_WIDTH, FRAME_HEIGHT

def main():
    print("Initializing Driver Drowsiness Detection System...")
    
    # Initialize components
    alerter = AudioAlerter()
    logger = IncidentLogger()
    evaluator = StateEvaluator(alerter, logger)
    
    print("Starting camera stream (Press 'q' to quit)...")
    
    with CameraStream() as cam, FaceLandmarkExtractor() as landmark_extractor:
        while True:
            success, frame = cam.read_frame()
            if not success:
                print("Failed to read from camera. Exiting...")
                break
                
            # Extract landmarks
            landmarks_2d, landmarks_3d = landmark_extractor.extract_landmarks(frame)
            
            # Default state text
            status_text = "Face Not Found"
            color = (0, 0, 255)
            
            if landmarks_2d is not None:
                # Compute metrics
                ear = compute_ear(landmarks_2d)
                mar = compute_mar(landmarks_2d)
                pitch, yaw, roll = compute_head_pose(landmarks_2d, FRAME_WIDTH, FRAME_HEIGHT)
                
                # Evaluate state and potentially trigger alerts
                status_text = evaluator.evaluate(ear, mar, pitch, yaw)
                
                if status_text == "Awake":
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255) # Red for alerts
                    
                # Visualize (draw landmarks and metrics)
                # Just draw some key points to save CPU, e.g. eyes and mouth
                # landmark_extractor.draw_landmarks(frame, landmarks_2d) # Un-comment to draw all
                
                # Display metrics on screen
                cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"MAR: {mar:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Pitch: {pitch:.0f} Yaw: {yaw:.0f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
            # Display status
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            cv2.imshow("Driver Drowsiness Detection", frame)
            
            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    # Cleanup
    alerter.release()
    cv2.destroyAllWindows()
    print("System gracefully shutdown.")

if __name__ == "__main__":
    main()
