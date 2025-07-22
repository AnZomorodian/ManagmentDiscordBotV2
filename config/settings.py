
import discord

# Bot Configuration
TOKEN = "MTAwMTQ1ODQ2NTk3NTMxMjQwNA.GPizIh.7PZQr5KhrvupPCcx6bIFescSpGXUxmychJ_MFo"
PREFIXES = ['!', '?', '$', '.']

# Discord Intents
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.voice_states = True
INTENTS.guilds = True
INTENTS.members = True
INTENTS.presences = True
INTENTS.moderation = True

# Voice Channel Settings
VOICE_SETTINGS = {
    "DEFAULT_BITRATE": 96000,  # Fixed: Discord's max bitrate is 96000, not 128000
    "DEFAULT_USER_LIMIT": 12,  # Increased from 10
    "CHANNEL_CHECK_INTERVAL": 15,
    "AUTO_DELETE_TIMEOUT": 300,  # 5 minutes
    "MAX_CHANNELS_PER_USER": 3,
    "VOICE_QUALITY_LEVELS": {
        "standard": 64000,
        "high": 96000,
        "premium": 128000  # Only for boosted servers
    }
}

# Bot Status Messages
BOT_ACTIVITIES = [
    {"type": "watching", "name": "for administrators | !help"},
    {"type": "listening", "name": "to server management | !admin"},
    {"type": "playing", "name": "Advanced Management Bot v3.0 | !setup"},
    {"type": "competing", "name": "Server Management Excellence | !moderation"},
    {"type": "watching", "name": "voice channels | !voicesettings"},
    {"type": "playing", "name": "with modular architecture | !botstats"}
]

# Fun Features
CHANNEL_NAMES = [
    "🎵 {}'s Lounge", "🎤 {}'s Studio", "🎮 {}'s Gaming Hub",
    "💭 {}'s Hangout", "🌟 {}'s Space", "🔥 {}'s Zone",
    "⚡ {}'s Room", "💎 {}'s Chamber", "🚀 {}'s Launch Pad",
    "🎯 {}'s Focus Room", "🎨 {}'s Creative Space", "🌙 {}'s Chill Zone",
    "🎪 {}'s Entertainment Hub", "🏰 {}'s Castle", "🌊 {}'s Wave Room"
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

# Color Schemes
COLORS = {
    "success": 0x00ff00,
    "error": 0xff0000,
    "warning": 0xffff00,
    "info": 0x0099ff,
    "admin": 0xffd700,
    "voice": 0x9932cc,
    "moderation": 0xff6600,
    "fun": 0xff69b4
}
