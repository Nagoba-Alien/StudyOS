"""
Global configuration for StudyOS.

All automation modules should read their
settings from this file.
"""

from pathlib import Path

# ==========================================
# General
# ==========================================

TIMEZONE = "Asia/Kolkata"

# ==========================================
# Daily Study Schedule
# ==========================================

DAILY_RUN_TIME = "08:00"

DEFAULT_STUDY_MINUTES = 60

# ==========================================
# Reports
# ==========================================

REPORTS_DIRECTORY = Path("reports")

# ==========================================
# Email
# ==========================================

EMAIL_ENABLED = True

# ==========================================
# Google Calendar
# ==========================================

GOOGLE_CALENDAR_ENABLED = True

# ==========================================
# Telegram
# ==========================================

TELEGRAM_ENABLED = False

# ==========================================
# Desktop Notifications
# ==========================================

NOTIFICATIONS_ENABLED = True
