import time
from src.evaluator import StateEvaluator

class MockAlerter:
    def __init__(self):
        self.triggered = False
    def trigger_alert(self):
        self.triggered = True

class MockLogger:
    def __init__(self):
        self.logs = []
    def log_incident(self, event_type, metric, duration):
        self.logs.append(event_type)

def test_evaluator_drowsiness():
    # Setup mocks and thresholds
    import src.config as config
    config.EAR_THRESHOLD = 0.25
    config.EAR_TIME_THRESHOLD = 1.0 # 1 second for faster test
    config.MAR_THRESHOLD = 0.6
    config.MAR_TIME_THRESHOLD = 1.0
    
    alerter = MockAlerter()
    logger = MockLogger()
    evaluator = StateEvaluator(alerter, logger)
    
    # Normal state
    status = evaluator.evaluate(ear=0.3, mar=0.1, pitch=0.0, yaw=0.0)
    assert status == "Awake"
    assert not alerter.triggered
    
    # Drowsy state starts
    status = evaluator.evaluate(ear=0.2, mar=0.1, pitch=0.0, yaw=0.0)
    assert status == "Awake" # Not triggered yet due to time window
    
    # Sleep to simulate time passing (just modifying the start_time is cleaner but this works)
    evaluator.ear_start_time = time.time() - 2.0 # Force time threshold
    
    status = evaluator.evaluate(ear=0.2, mar=0.1, pitch=0.0, yaw=0.0)
    assert status == "DROWSINESS DETECTED"
    assert alerter.triggered
    assert "DROWSINESS" in logger.logs
