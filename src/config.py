
# Video Capture Settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Drowsiness Detection Thresholds
EAR_THRESHOLD = 0.25      # Eye Aspect Ratio threshold below which eye is considered closed
EAR_TIME_THRESHOLD = 2.5  # Seconds for EAR < THRESHOLD to trigger drowsiness alert

# Yawning Detection Thresholds
MAR_THRESHOLD = 0.65      # Mouth Aspect Ratio threshold above which mouth is considered open
MAR_TIME_THRESHOLD = 2.0  # Seconds for MAR > THRESHOLD to trigger yawn alert

# Head Pose Detection Thresholds
HEAD_PITCH_THRESHOLD_DOWN = -20.0  # Degrees, head nodding down
HEAD_YAW_THRESHOLD_LEFT = -30.0    # Degrees, looking left
HEAD_YAW_THRESHOLD_RIGHT = 30.0    # Degrees, looking right
HEAD_TIME_THRESHOLD = 3.0          # Seconds for head pose threshold to trigger distraction alert

# MediaPipe Face Mesh settings
MAX_NUM_FACES = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Landmark indices for MediaPipe Face Mesh
# Eyes
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Mouth
LIPS = [61, 291, 39, 181, 0, 17, 269, 405]
MOUTH_OUTER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]
MOUTH_INNER = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311, 312, 13, 82, 81, 42, 183]

# Key points for Head Pose (PnP)
# Nose tip, Chin, Left eye left corner, Right eye right corner, Left Mouth corner, Right mouth corner
FACE_3D_LANDMARKS = [1, 152, 33, 263, 61, 291]
