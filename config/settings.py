import os
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN not found in .env file!")

PREFIXES = ['!', '?', '.']
INTENTS = discord.Intents.all()

# Voice Channel Settings
VOICE_SETTINGS = {
    "VOICE_QUALITY_LEVELS": {
        "standard": 64000,    # Standard quality (64kbps)
        "high": 128000,       # High quality (128kbps)
        "premium": 256000     # Premium quality (256kbps)
    },
    "DEFAULT_USER_LIMIT": 0,  # 0 = no limit
    "AUTO_DELETE_TIMEOUT": 300,  # 5 minutes
    "MAX_CHANNELS_PER_USER": 3
}

# Channel Name Templates
CHANNEL_NAMES = [
    "{}'s Room",
    "{}'s Hangout", 
    "{}'s Voice Chat",
    "{}'s Space",
    "{}'s Channel",
    "{}'s Lounge",
    "🎵 {}'s Music Room",
    "🎮 {}'s Gaming Room",
    "💬 {}'s Chat Room",
    "🎯 {}'s Focus Room",
    "🎨 {}'s Creative Space",
    "🌙 {}'s Chill Zone",
    "🎪 {}'s Entertainment Hub",
    "🏰 {}'s Castle",
    "🌊 {}'s Wave Room"
]

# Magic 8-Ball Responses
EIGHT_BALL_RESPONSES = [
    "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
    "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
    "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
    "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
    "Don't count on it", "My reply is no", "My sources say no",
    "Outlook not so good", "Very doubtful", "Absolutely not", "The stars say no"
]

# Embed Colors
COLORS = {
    "success": 0x00ff00,   # Green
    "error": 0xff0000,     # Red  
    "warning": 0xffff00,   # Yellow
    "info": 0x00ffff,      # Cyan
    "admin": 0xff00ff,     # Magenta
    "voice": 0x9932cc,     # Purple
    "moderation": 0xff6600, # Orange
    "fun": 0xff69b4        # Pink
}

# Bot Status Messages
BOT_ACTIVITIES = [
    {"type": "watching", "name": "for administrators | !help"},
    {"type": "listening", "name": "to server management | !admin"},
    {"type": "playing", "name": "Amazing Management Bot v3.1 | !setup"},
    {"type": "competing", "name": "Server Management Excellence | !moderation"},
    {"type": "watching", "name": "voice channels | !voicesettings"},
    {"type": "playing", "name": "with secure .env configuration | !botstats"}
]

# Rate Limiting Settings
RATE_LIMITS = {
    "commands_per_minute": 30,
    "channels_per_hour": 10,
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