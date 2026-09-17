import cv2
import mediapipe as mp
import numpy as np
from .config import MAX_NUM_FACES, MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE

class FaceLandmarkExtractor:
    """Extracts 468 facial landmarks using MediaPipe Face Mesh."""

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=MAX_NUM_FACES,
            refine_landmarks=True, # Needed for iris tracking if required, and better lip/eye points
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

    def extract_landmarks(self, frame):
        """
        Processes a BGR frame and returns facial landmarks.

        Args:
            frame (np.ndarray): BGR image frame from OpenCV.

        Returns:
            landmarks_2d (np.ndarray or None): 2D pixel coordinates of landmarks (N, 2), or None if no face found.
            landmarks_3d (np.ndarray or None): 3D coordinates (x, y, z) normalized, or None if no face found.
        """
        # Convert BGR to RGB as MediaPipe requires RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        rgb_frame.flags.writeable = False
        results = self.face_mesh.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.multi_face_landmarks:
            return None, None

        # Process the first face found
        face_landmarks = results.multi_face_landmarks[0]
        
        h, w, _ = frame.shape
        
        landmarks_2d = []
        landmarks_3d = []
        
        for lm in face_landmarks.landmark:
            # 2D coordinates scaled to image dimensions
            x, y = int(lm.x * w), int(lm.y * h)
            landmarks_2d.append([x, y])
            
            # 3D coordinates (normalized)
            landmarks_3d.append([lm.x, lm.y, lm.z])
            
        return np.array(landmarks_2d), np.array(landmarks_3d)

    def draw_landmarks(self, frame, landmarks_2d, indices=None, color=(0, 255, 0)):
        """Utility to draw specific landmarks on the frame."""
        if landmarks_2d is None:
            return
            
        pts = landmarks_2d if indices is None else landmarks_2d[indices]
        for (x, y) in pts:
            cv2.circle(frame, (x, y), 1, color, -1)
            
    def release(self):
        """Close the MediaPipe Face Mesh instance."""
        self.face_mesh.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
