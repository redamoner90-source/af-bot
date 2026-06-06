#!/usr/bin/env python3
"""
Configuration module for AF Bot
Loads settings from .env file or environment variables
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# =============================================================================
# Telegram Configuration
# =============================================================================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID', '')

if not TELEGRAM_BOT_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN not set!")
    print("   Set it in environment variables or .env file")
    sys.exit(1)

# =============================================================================
# AppsFlyer Configuration
# =============================================================================
APPSFLYER_DEV_KEY = os.getenv('APPSFLYER_DEV_KEY', '')

if not APPSFLYER_DEV_KEY:
    print("❌ Error: APPSFLYER_DEV_KEY not set!")
    print("   Set it in environment variables or .env file")
    sys.exit(1)

# =============================================================================
# Proxy Configuration
# =============================================================================
USE_PROXY = int(os.getenv('USE_PROXY', 0))
PROXY_IP_PORT = os.getenv('PROXY_IP_PORT', '')
PROXY_USERNAME = os.getenv('PROXY_USERNAME', '')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', '')

# =============================================================================
# Bot Settings
# =============================================================================
SHOW_RESPONSE = int(os.getenv('SHOW_RESPONSE', 1))
LOG_FILE = os.getenv('LOG_FILE', 'data/af_events.log')
DEBUG_MODE = int(os.getenv('DEBUG_MODE', 0))

# =============================================================================
# Data Files
# =============================================================================
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / 'users.json'
SCHEDULED_TASKS_FILE = DATA_DIR / 'scheduled_tasks.json'
AF_CONFIG_FILE = DATA_DIR / 'af_config.json'
GAMES_FILE = DATA_DIR / 'games.json'

# =============================================================================
# Default Values
# =============================================================================
DEFAULT_PURCHASE_EVENT = "af_purchase"
DEFAULT_CURRENCY = "USD"
DEFAULT_CONTENT_ID = "Emeralds"

PRESET_AMOUNTS = [0.99, 1.99, 4.99, 9.99, 19.99, 49.99, 99.99]

# =============================================================================
# Scheduling Configuration
# =============================================================================
TIMEZONE = 'UTC'  # Change to your timezone (e.g., 'Asia/Damascus')
SCHEDULER_JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1,
}

# =============================================================================
# UI Messages
# =============================================================================
WELCOME_MESSAGE = """
🚀 **مرحباً في AF Bot**

هذا البوت يساعدك على إدارة أحداث AppsFlyer بسهولة!

اختر من القائمة أدناه لبدء العمل.
"""

MENU_MESSAGE = """
📋 **القائمة الرئيسية**

اختر ما تريد:

1️⃣ إرسال حدث
2️⃣ جدولة حدث
3️⃣ الإعدادات
4️⃣ السجلات
5️⃣ المساعدة
"""

HELP_MESSAGE = """
📚 **المساعدة والشرح**

**إرسال حدث:**
اختر الحدث وأدخل التفاصيل اللازمة

**جدولة حدث:**
حدد الحدث والتكرار والوقت

**الإعدادات:**
أضف أو عدّل GAID و AF UID

**السجلات:**
اعرض آخر الأحداث المرسلة

للمزيد من المساعدة، تواصل مع الدعم.
"""

print("✅ Configuration loaded successfully!")
