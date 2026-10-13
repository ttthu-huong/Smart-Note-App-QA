"""Configuration settings for Smart Note App Automation Testing."""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_ROOT = os.path.join(PROJECT_ROOT, "evidence")
REPORTS_ROOT = os.path.join(PROJECT_ROOT, "automation", "reports")

# Android Device Settings
DEVICE_SERIAL = os.getenv("DEVICE_SERIAL", "R5CW82ECF6M")
APP_PACKAGE = "com.example.smart_note_app"
APP_ACTIVITY = ".MainActivity"

# Test Timing
DEFAULT_TIMEOUT = 10
NETWORK_WAIT = 3.5
ANIMATION_WAIT = 0.5
