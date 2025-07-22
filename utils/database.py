
# Data storage for the bot
created_channels = {}
user_stats = {}
guild_settings = {}
moderation_logs = {}

def initialize_data():
    """Initialize all data storage"""
    global created_channels, user_stats, guild_settings, moderation_logs
    created_channels = {}
    user_stats = {}
    guild_settings = {}
    moderation_logs = {}
    print("📊 Data storage initialized")

def load_guild_settings(guild_id):
    """Load or create guild settings"""
    if guild_id not in guild_settings:
        guild_settings[guild_id] = {
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
            "moderation_enabled": True
        }
    return guild_settings[guild_id]

def get_user_stats(user_id):
    """Get or create user statistics"""
    if user_id not in user_stats:
        user_stats[user_id] = {
            "channels_created": 0,
            "total_time": 0,
            "commands_used": 0,
            "last_active": None,
            "achievements": [],
            "messages_sent": 0,
            "voice_joins": 0,
            "favorite_channel": None
        }
    return user_stats[user_id]

def update_user_command_stats(user_id):
    """Update user command usage statistics"""
    stats = get_user_stats(user_id)
    stats["commands_used"] += 1
    import datetime
    stats["last_active"] = datetime.datetime.now().isoformat()id]

def add_moderation_log(guild_id, action, moderator, target, reason):
    """Add a moderation log entry"""
    if guild_id not in moderation_logs:
        moderation_logs[guild_id] = []
    
    import datetime
    log_entry = {
        "timestamp": datetime.datetime.now(),
        "action": action,
        "moderator": moderator,
        "target": target,
        "reason": reason
    }
    moderation_logs[guild_id].append(log_entry)
    
    # Keep only last 100 logs per guild
    if len(moderation_logs[guild_id]) > 100:
        moderation_logs[guild_id] = moderation_logs[guild_id][-100:]

def get_moderation_logs(guild_id, limit=10):
    """Get recent moderation logs"""
    if guild_id not in moderation_logs:
        return []
    return moderation_logs[guild_id][-limit:]
