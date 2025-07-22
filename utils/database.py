
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

def update_user_channel_creation(user_id):
    """Update user channel creation count"""
    stats = get_user_stats(user_id)
    stats["channels_created"] += 1
    import datetime
    stats["last_active"] = datetime.datetime.now().isoformat()
    print(f"📊 Updated channel creation for user {user_id}")

def update_user_voice_time(user_id, minutes):
    """Update user voice time"""
    stats = get_user_stats(user_id)
    stats["total_time"] += minutes
    stats["voice_joins"] += 1
    import datetime
    stats["last_active"] = datetime.datetime.now().isoformat()

def update_user_message_count(user_id):
    """Update user message count"""
    stats = get_user_stats(user_id)
    stats["messages_sent"] += 1
    import datetime
    stats["last_active"] = datetime.datetime.now().isoformat()

def get_top_users(limit=10):
    """Get top users by channel creation"""
    sorted_users = sorted(
        user_stats.items(), 
        key=lambda x: x[1]['channels_created'], 
        reverse=True
    )
    return sorted_users[:limit]

def get_guild_stats():
    """Get overall guild statistics"""
    total_channels = sum(stats['channels_created'] for stats in user_stats.values())
    total_commands = sum(stats['commands_used'] for stats in user_stats.values())
    total_voice_time = sum(stats['total_time'] for stats in user_stats.values())
    
    return {
        "total_channels_created": total_channels,
        "total_commands_used": total_commands,
        "total_voice_time": total_voice_time,
        "active_users": len(user_stats),
        "active_channels": len(created_channels)
    }

def update_user_command_stats(user_id):
    """Update user command usage statistics"""
    stats = get_user_stats(user_id)
    stats["commands_used"] += 1
    import datetime
    stats["last_active"] = datetime.datetime.now().isoformat()

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

def save_guild_settings(guild_id, settings):
    """Save guild settings to local storage"""
    guild_settings[guild_id] = settings
    print(f"💾 Settings saved for guild {guild_id}")
