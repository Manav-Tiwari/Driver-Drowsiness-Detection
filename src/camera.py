import cv2
from .config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, FPS

class CameraStream:
    """Handles the video stream from the webcam."""

    def __init__(self, camera_index=CAMERA_INDEX):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Try to set resolution and FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera with index {self.camera_index}")

    def read_frame(self):
        """Reads a frame from the camera.
        Returns:
            success (bool): Whether the frame was read successfully.
            frame (np.ndarray): The captured frame in BGR format.
        """
        success, frame = self.cap.read()
        return success, frame

    def release(self):
        """Releases the camera resource."""
        if self.cap.isOpened():
            self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
