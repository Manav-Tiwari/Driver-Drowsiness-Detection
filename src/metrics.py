import numpy as np
import cv2
from scipy.spatial import distance
from .config import LEFT_EYE, RIGHT_EYE, MOUTH_INNER, FACE_3D_LANDMARKS

def compute_aspect_ratio(landmarks, indices):
    """
    Generic function to compute aspect ratio for eyes or mouth.
    Formula: (|p2 - p6| + |p3 - p5|) / (2 * |p1 - p4|)
    """
    if landmarks is None or len(indices) < 6:
        return 0.0
        
    pts = landmarks[indices]
    
    # Compute the euclidean distances between the two sets of vertical landmarks
    A = distance.euclidean(pts[1], pts[5])
    B = distance.euclidean(pts[2], pts[4])
    
    # Compute the euclidean distance between the horizontal landmarks
    C = distance.euclidean(pts[0], pts[3])
    
    if C == 0:
        return 0.0
        
    # Compute the aspect ratio
    ratio = (A + B) / (2.0 * C)
    return ratio

def compute_ear(landmarks_2d):
    """Computes the average Eye Aspect Ratio (EAR) for both eyes."""
    if landmarks_2d is None:
        return 0.0
    
    left_ear = compute_aspect_ratio(landmarks_2d, LEFT_EYE)
    right_ear = compute_aspect_ratio(landmarks_2d, RIGHT_EYE)
    
    # Average the EAR of both eyes
    return (left_ear + right_ear) / 2.0

def compute_mar(landmarks_2d):
    """
    Computes Mouth Aspect Ratio (MAR).
    Uses the inner lip landmarks for better yawning detection.
    For the mouth, the indices structure differs slightly from the eye.
    Using specific points: 
    Horizontal: 0 and 6 (corners of the mouth)
    Vertical: 2 and 6 (top and bottom), 3 and 5.
    (Note: MOUTH_INNER has 20 points, we will use a simplified calculation 
     based on the key points: corners, top mid, bottom mid).
    """
    if landmarks_2d is None:
        return 0.0
    
    # Using specific indices from the inner lip loop (20 points total)
    # 0: Left corner, 10: Right corner
    # 3, 4, 5: Top inner lip
    # 15, 14, 13: Bottom inner lip
    pts = landmarks_2d[MOUTH_INNER]
    
    A = distance.euclidean(pts[3], pts[17]) # Vertical distance 1
    B = distance.euclidean(pts[5], pts[15]) # Vertical distance 2
    C = distance.euclidean(pts[0], pts[10]) # Horizontal distance (width)
    
    if C == 0:
        return 0.0
        
    mar = (A + B) / (2.0 * C)
    return mar

def compute_head_pose(landmarks_2d, frame_width, frame_height):
    """
    Computes the head pose angles (pitch, yaw, roll) using PnP.
    Returns:
        pitch (float): Nodding up/down (positive is down)
        yaw (float): Looking left/right (positive is right)
        roll (float): Tilting head left/right
    """
    if landmarks_2d is None:
        return 0.0, 0.0, 0.0
        
    # Extract the 2D keypoints
    image_pts = np.array(landmarks_2d[FACE_3D_LANDMARKS], dtype="double")
    
    # Generic 3D model points (in arbitrary units, roughly corresponding to a typical human face)
    # Nose tip, Chin, Left eye left corner, Right eye right corner, Left mouth corner, Right mouth corner
    model_pts = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ])
    
    # Camera internals
    focal_length = frame_width
    center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    
    dist_coeffs = np.zeros((4, 1)) # Assume no lens distortion
    
    success, rotation_vec, translation_vec = cv2.solvePnP(
        model_pts, image_pts, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    
    if not success:
        return 0.0, 0.0, 0.0
        
    # Get rotational matrix
    rmat, _ = cv2.Rodrigues(rotation_vec)
    
    # Get angles from rotational matrix using Euler angles formulation
    # pitch, yaw, roll
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    
    pitch = angles[0]
    yaw = angles[1]
    roll = angles[2]
    
    return pitch, yaw, roll
