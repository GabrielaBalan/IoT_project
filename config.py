YOUTUBE_URL = "https://www.youtube.com/watch?v=DsNtwGJXTTs"
MODEL_PATH = "yolov8n.pt"

CONF_THRESHOLD = 0.50
LARGE_GROUP_THRESHOLD = 3
VISIT_GAP_SECONDS = 10
SAVE_ANALYTICS_ON_EXIT = True

SAVE_FRAMES = True
FRAMES_DIR = "saved_frames"
EVENT_IMAGE_COOLDOWN_SECONDS = 10
DETECTIONS_CSV = "detections.csv"
FRAME_SUMMARY_CSV = "frame_summary.csv"
EVENTS_CSV = "events.csv"
VISITS_CSV = "visits.csv"
ZONE_USAGE_CSV = "zone_usage.csv"
CO_OCCURRENCE_CSV = "co_occurrence.csv"
SESSION_SUMMARY_TXT = "session_summary.txt"

CLASS_MAPPING = {
    "elephant": "elephant",
    "zebra": "zebra",
    "giraffe": "giraffe",
    "bird": "bird",
    "cow": "ungulate",
    "horse": "ungulate",
}