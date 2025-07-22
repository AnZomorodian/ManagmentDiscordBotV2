
import os
import discord
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

# Bot Configuration
BOT_VERSION = "3.1"
BOT_AUTHOR = "Amazing Bot Team"
BOT_DESCRIPTION = "Professional Discord Management Bot with .env Security"

# Command Prefixes
PREFIXES = ['!', '?', '.', PREFIX]

# Discord Intents
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True
INTENTS.voice_states = True
INTENTS.guilds = True
INTENTS.guild_messages = True

# Bot Activities for Status Rotation
BOT_ACTIVITIES = [
    {"type": "watching", "name": "over {} servers"},
    {"type": "listening", "name": "your commands"},
    {"type": "playing", "name": "with Discord API v3.1"},
    {"type": "watching", "name": "for !help commands"},
    {"type": "listening", "name": "to community feedback"},
    {"type": "playing", "name": "Amazing Management v3.1"}
]

# Color Scheme
COLORS = {
    "success": 0x00FF00,
    "error": 0xFF0000,
    "warning": 0xFFA500,
    "info": 0x3498DB,
    "admin": 0x9B59B6,
    "mod": 0xE74C3C,
    "premium": 0xFFD700
}

# Voice Channel Settings
VOICE_SETTINGS = {
    "VOICE_QUALITY_LEVELS": {
        "low": 32000,
        "medium": 64000,
        "high": 96000,
        "premium": 128000
    },
    "DEFAULT_BITRATE": 64000,
    "MAX_USER_CHANNELS": 5
}

# Fun Channel Names for Auto Voice
CHANNEL_NAMES = [
    "{}'s Room",
    "{}'s Hangout", 
    "{}'s Space",
    "{}'s Voice Chat",
    "{}'s Meeting Room",
    "{}'s Gaming Room",
    "{}'s Study Hall",
    "{}'s Music Room"
]

# Security Settings
SECURITY = {
    "max_warnings": 3,
    "auto_ban_threshold": 5,
    "spam_detection": True,
    "raid_protection": True,
    "auto_mod": True,
    "link_protection": True,
    "mention_spam_limit": 5,
    "messages_per_minute": 20
}

# Feature Flags
FEATURES = {
    "auto_voice": True,
    "moderation": True,
    "welcome_system": True,
    "statistics": True,
    "fun_commands": True,
    "auto_roles": True,
    "enhanced_security": True
}

# Default Guild Settings Template
DEFAULT_GUILD_SETTINGS = {
    "auto_voice": True,
    "welcome_channel": None,
    "log_channel": None, 
    "auto_role": None,
    "banned_words": [],
    "max_channels_per_user": 3,
    "trigger_channels": [],
    "voice_quality": "high",
    "auto_delete_timeout": 300,
    "welcome_message": True,
    "moderation_enabled": True,
    "prefix": "!",
    "language": "en"
}

# Validation
if TOKEN:
    print(f"✅ Configuration loaded successfully from .env")
    print(f"🔐 Token validation: {'✅ Valid' if len(TOKEN) > 50 else '❌ Invalid'}")
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
    print("💡 Please add your bot token to the .env file")
