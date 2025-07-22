# Simple in-memory storage without complex database features

# Simple counters for basic functionality
command_usage = {}
user_activity = {}

def get_user_stats(user_id):
    """Get basic user stats"""
    if user_id not in user_activity:
        user_activity[user_id] = {
            "commands_used": 0,
            "channels_created": 0,
            "voice_joins": 0,
            "messages_sent": 0,
            "total_time": 0,
            "last_active": None
        }
    return user_activity[user_id]

def update_user_command_stats(user_id):
    """Update command usage"""
    stats = get_user_stats(user_id)
    stats["commands_used"] += 1

def load_guild_settings(guild_id):
    """Load basic guild settings"""
    return {
        "auto_voice": True,
        "welcome_channel": None,
        "log_channel": None,
        "trigger_channels": [],
        "prefix": "!"
    }

def save_guild_settings(guild_id, settings):
    """Save guild settings - simplified"""
    pass

# Simple storage for created channels
created_channels = {}