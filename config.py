#!/usr/bin/env python3
"""Shared configuration - loads from environment variables with hardcoded fallbacks."""
import os

API_ID       = int(os.environ.get("TELEGRAM_API_ID", "39040426"))
API_HASH     = os.environ.get("TELEGRAM_API_HASH", "6e6ab2a82b7401ab1513729593a86b1d")
SESSION      = os.environ.get("TELEGRAM_SESSION", "/home/david/smarthome_session")
BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "8616021483:AAHHslNjxDayDVfoXcGbYsvStAdoa3_D1Bo")
CHAT_ID      = os.environ.get("TELEGRAM_CHAT_ID", "303984494")
BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME", "zaltsman_assistant_bot")
PHONE        = os.environ.get("TELEGRAM_PHONE", "+972542020184")
