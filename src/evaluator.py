import time
from .config import (
    EAR_THRESHOLD, EAR_TIME_THRESHOLD,
    MAR_THRESHOLD, MAR_TIME_THRESHOLD,
    HEAD_PITCH_THRESHOLD_DOWN, HEAD_YAW_THRESHOLD_LEFT, HEAD_YAW_THRESHOLD_RIGHT, HEAD_TIME_THRESHOLD
)

class StateEvaluator:
    """
    Evaluates driver state based on temporally smoothed metrics.
    Prevents false positives by requiring a threshold to be breached continuously for X seconds.
    """
    
    def __init__(self, alerter, logger):
        self.alerter = alerter
        self.logger = logger
        
        # State tracking
        self.ear_start_time = None
        self.mar_start_time = None
        self.head_start_time = None
        
        # Cooldown to prevent spamming logs
        self.last_log_time = 0
        self.log_cooldown = 5.0 # seconds

    def evaluate(self, ear, mar, pitch, yaw):
        """
        Takes current metrics and evaluates if an alert should be triggered.
        """
        current_time = time.time()
        alert_triggered = False
        status_text = "Awake"
        
        # 1. Drowsiness Evaluation (EAR)
        if ear < EAR_THRESHOLD:
            if self.ear_start_time is None:
                self.ear_start_time = current_time
            else:
                duration = current_time - self.ear_start_time
                if duration >= EAR_TIME_THRESHOLD:
                    self.alerter.trigger_alert()
                    status_text = "DROWSINESS DETECTED"
                    alert_triggered = True
                    self._log_incident("DROWSINESS", ear, duration, current_time)
        else:
            self.ear_start_time = None

        # 2. Yawning Evaluation (MAR)
        if mar > MAR_THRESHOLD:
            if self.mar_start_time is None:
                self.mar_start_time = current_time
            else:
                duration = current_time - self.mar_start_time
                if duration >= MAR_TIME_THRESHOLD:
                    # Yawning is a sign of fatigue, we might just warn
                    self.alerter.trigger_alert()
                    if not alert_triggered:
                        status_text = "YAWNING DETECTED"
                        alert_triggered = True
                    self._log_incident("YAWNING", mar, duration, current_time)
        else:
            self.mar_start_time = None
            
        # 3. Distraction Evaluation (Head Pose)
        is_distracted = (
            pitch < HEAD_PITCH_THRESHOLD_DOWN or 
            yaw < HEAD_YAW_THRESHOLD_LEFT or 
            yaw > HEAD_YAW_THRESHOLD_RIGHT
        )
        
        if is_distracted:
            if self.head_start_time is None:
                self.head_start_time = current_time
            else:
                duration = current_time - self.head_start_time
                if duration >= HEAD_TIME_THRESHOLD:
                    self.alerter.trigger_alert()
                    if not alert_triggered:
                        status_text = "DISTRACTION DETECTED"
                    self._log_incident("DISTRACTION", yaw, duration, current_time)
        else:
            self.head_start_time = None

        return status_text

    def _log_incident(self, event_type, metric_value, duration, current_time):
        """Helper to log incidents with a cooldown to avoid spamming the DB."""
        if current_time - self.last_log_time > self.log_cooldown:
            self.logger.log_incident(event_type, metric_value, duration)
            self.last_log_time = current_time
