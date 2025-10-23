import random
import time
from datetime import datetime, timedelta
import json
import os

class DataManager:
    """Data manager for gunshot detection data"""
    
    def __init__(self):
        self.detection_data = []
        self.data_file = "detection_data.json"
        self.load_data()
    
    def load_data(self):
        """Load detection data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.detection_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.detection_data = []
        else:
            # Generate some sample data for testing
            self.generate_sample_data()
    
    def save_data(self):
        """Save detection data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.detection_data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def generate_sample_data(self):
        """Generate sample detection data for testing"""
        current_time = time.time()
        
        # Generate detections for the last 24 hours
        for i in range(20):
            detection_time = current_time - random.randint(0, 86400)  # Last 24 hours
            
            detection = {
                "id": f"DET_{int(detection_time)}_{i}",
                "timestamp": detection_time,
                "latitude": 40.7128 + random.uniform(-0.01, 0.01),  # NYC area
                "longitude": -74.0060 + random.uniform(-0.01, 0.01),
                "intensity": random.uniform(0.3, 1.0),
                "confidence": random.uniform(0.7, 0.99),
                "angle": random.randint(0, 359),
                "distance": random.randint(10, 100),
                "audio_file": f"audio_{int(detection_time)}.wav",
                "verified": random.choice([True, False, None])
            }
            
            self.detection_data.append(detection)
        
        # Sort by timestamp (newest first)
        self.detection_data.sort(key=lambda x: x["timestamp"], reverse=True)
        self.save_data()
    
    def add_detection(self, detection_data):
        """Add a new detection"""
        detection_data["id"] = f"DET_{int(time.time())}_{len(self.detection_data)}"
        detection_data["timestamp"] = time.time()
        
        self.detection_data.insert(0, detection_data)  # Add to beginning
        self.save_data()
        return detection_data["id"]
    
    def get_recent_detections(self, limit=10):
        """Get recent detections for radar display"""
        recent = self.detection_data[:limit]
        
        # Convert to radar format
        radar_points = []
        for detection in recent:
            radar_points.append({
                "angle": detection["angle"],
                "distance": detection["distance"],
                "intensity": detection["intensity"],
                "timestamp": detection["timestamp"],
                "id": detection["id"]
            })
        
        return radar_points
    
    def get_detection_count_today(self):
        """Get count of detections today"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_timestamp = today_start.timestamp()
        
        count = sum(1 for d in self.detection_data if d["timestamp"] >= today_timestamp)
        return count
    
    def get_recent_detection_list(self, limit=10):
        """Get recent detections as formatted strings"""
        recent = self.detection_data[:limit]
        formatted_list = []
        
        for detection in recent:
            dt = datetime.fromtimestamp(detection["timestamp"])
            time_str = dt.strftime("%H:%M:%S")
            intensity_str = f"{detection['intensity']:.1f}"
            confidence_str = f"{detection['confidence']:.0%}"
            
            formatted_list.append(
                f"{time_str} | Int: {intensity_str} | Conf: {confidence_str}"
            )
        
        return formatted_list
    
    def get_map_detections(self, time_filter="Last 24 Hours", min_intensity=0.0):
        """Get detections for map display with filters"""
        # Calculate time threshold
        now = time.time()
        time_thresholds = {
            "Last Hour": now - 3600,
            "Last 24 Hours": now - 86400,
            "Last Week": now - 604800,
            "Last Month": now - 2592000
        }
        
        threshold = time_thresholds.get(time_filter, now - 86400)
        
        # Filter detections
        filtered = [
            d for d in self.detection_data
            if d["timestamp"] >= threshold and d["intensity"] >= min_intensity
        ]
        
        # Format for display
        formatted_list = []
        for detection in filtered:
            dt = datetime.fromtimestamp(detection["timestamp"])
            time_str = dt.strftime("%m/%d %H:%M")
            lat_str = f"{detection['latitude']:.4f}"
            lon_str = f"{detection['longitude']:.4f}"
            intensity_str = f"{detection['intensity']:.2f}"
            
            formatted_list.append(
                f"{time_str} | {lat_str}, {lon_str} | Int: {intensity_str}"
            )
        
        return formatted_list
    
    def get_detection_by_id(self, detection_id):
        """Get specific detection by ID"""
        for detection in self.detection_data:
            if detection["id"] == detection_id:
                return detection
        return None
    
    def update_detection(self, detection_id, updates):
        """Update detection data"""
        for i, detection in enumerate(self.detection_data):
            if detection["id"] == detection_id:
                self.detection_data[i].update(updates)
                self.save_data()
                return True
        return False
    
    def delete_detection(self, detection_id):
        """Delete a detection"""
        self.detection_data = [
            d for d in self.detection_data if d["id"] != detection_id
        ]
        self.save_data()
    
    def get_statistics(self):
        """Get detection statistics"""
        if not self.detection_data:
            return {
                "total": 0,
                "today": 0,
                "avg_intensity": 0,
                "avg_confidence": 0
            }
        
        total = len(self.detection_data)
        today = self.get_detection_count_today()
        
        avg_intensity = sum(d["intensity"] for d in self.detection_data) / total
        avg_confidence = sum(d["confidence"] for d in self.detection_data) / total
        
        return {
            "total": total,
            "today": today,
            "avg_intensity": avg_intensity,
            "avg_confidence": avg_confidence
        }
    
    def clear_old_data(self, days_to_keep=30):
        """Clear detection data older than specified days"""
        cutoff_time = time.time() - (days_to_keep * 86400)
        
        self.detection_data = [
            d for d in self.detection_data if d["timestamp"] >= cutoff_time
        ]
        self.save_data()