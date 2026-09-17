import sqlite3
import datetime
import os

class IncidentLogger:
    """Logs drowsiness and distraction incidents to a local SQLite database."""
    
    def __init__(self, db_path="incidents.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize the database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                metric_value REAL NOT NULL,
                duration REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_incident(self, event_type, metric_value, duration):
        """
        Logs a new incident.
        
        Args:
            event_type (str): "DROWSINESS", "YAWNING", or "DISTRACTION"
            metric_value (float): The value of the metric that triggered the incident (e.g., EAR)
            duration (float): How long the event lasted before triggering
        """
        timestamp = datetime.datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO incidents (timestamp, event_type, metric_value, duration)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, event_type, metric_value, duration))
        
        conn.commit()
        conn.close()
        
    def get_all_incidents(self):
        """Retrieve all logged incidents."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM incidents ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        conn.close()
        return rows
