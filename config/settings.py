import os
import discord
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIXES = ['!', '?', '.']
BOT_VERSION = "3.2"

# Enhanced Discord Intents
INTENTS = discord.Intents.all()

# Voice Channel Settings
VOICE_SETTINGS = {
    'auto_delete_timeout': 300,  # 5 minutes
    'max_user_channels': 3,
    'default_bitrate': 64000,
    'max_bitrate': 256000,
    'default_user_limit': 0
}

# Channel Names for Auto-Creation
CHANNEL_NAMES = [
    "{}'s Room",
    "{}'s Hangout",
    "{}'s Space",
    "{}'s Channel",
    "{}'s Voice",
    "{}'s Zone",
    "{}'s Chat"
]

# Embed Colors
EMBED_COLORS = {
    'success': 0x00ff00,
    'error': 0xff0000,
    'warning': 0xffff00,
    'info': 0x00ffff,
    'primary': 0x0099ff,
    'secondary': 0x9932cc
}

# Bot Status Messages
STATUS_MESSAGES = [
    f"Amazing Bot v{BOT_VERSION}",
    "Serving multiple servers!",
    "Type !help for commands",
    "Managing your Discord!",
    "🎵 Voice channels ready!"
]

def validate_environment():
    """Validate environment configuration"""
    if not TOKEN:
        print("❌ DISCORD_TOKEN not found in environment variables!")
        return False

    if len(TOKEN) < 50:
        print("❌ Invalid Discord token format!")
        return False

    print("✅ Environment validation passed!")
    return True