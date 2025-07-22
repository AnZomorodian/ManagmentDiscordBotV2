
import json
import datetime
from typing import Dict, List, Any, Optional

# In-memory storage for local data persistence
guild_settings: Dict[int, Dict[str, Any]] = {}
user_stats: Dict[int, Dict[str, Any]] = {}
moderation_logs: Dict[int, List[Dict[str, Any]]] = {}
server_analytics: Dict[int, Dict[str, Any]] = {}

def initialize_data():
    """Initialize all data storage systems"""
    print("📊 Data storage initialized")
    print("💾 Local storage system active")
    print("🗄️ In-memory database ready")

def load_guild_settings(guild_id: int) -> Dict[str, Any]:
    """Load guild settings from local storage"""
    if guild_id not in guild_settings:
        from config.settings import DEFAULT_GUILD_SETTINGS
        guild_settings[guild_id] = DEFAULT_GUILD_SETTINGS.copy()
    return guild_settings[guild_id]

def save_guild_settings(guild_id: int, settings: Dict[str, Any]):
    """Save guild settings to local storage"""
    guild_settings[guild_id] = settings
    print(f"💾 Settings saved for guild {guild_id}")

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get user statistics"""
    if user_id not in user_stats:
        user_stats[user_id] = {
            "commands_used": 0,
            "messages_sent": 0,
            "voice_time": 0,
            "level": 1,
            "xp": 0,
            "last_active": None,
            "warnings": 0,
            "coins": 100
        }
    return user_stats[user_id]

def update_user_stats(user_id: int, stat_type: str, value: int = 1):
    """Update user statistics"""
    stats = get_user_stats(user_id)
    if stat_type in stats:
        if isinstance(stats[stat_type], int):
            stats[stat_type] += value
        else:
            stats[stat_type] = value
    stats["last_active"] = datetime.datetime.now().isoformat()

def update_user_command_stats(user_id: int):
    """Update user command usage statistics"""
    stats = get_user_stats(user_id)
    stats["commands_used"] += 1
    stats["last_active"] = datetime.datetime.now().isoformat()

def add_moderation_log(guild_id: int, action: str, moderator: int, target: int, reason: str):
    """Add a moderation log entry"""
    if guild_id not in moderation_logs:
        moderation_logs[guild_id] = []
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "moderator": moderator,
        "target": target,
        "reason": reason,
        "id": len(moderation_logs[guild_id]) + 1
    }
    
    moderation_logs[guild_id].append(log_entry)
    print(f"📝 Moderation log added: {action} by {moderator} on {target}")

def get_moderation_logs(guild_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Get moderation logs for a guild"""
    if guild_id not in moderation_logs:
        return []
    return moderation_logs[guild_id][-limit:]

def get_server_analytics(guild_id: int) -> Dict[str, Any]:
    """Get server analytics"""
    if guild_id not in server_analytics:
        server_analytics[guild_id] = {
            "total_commands": 0,
            "total_messages": 0,
            "active_users": set(),
            "voice_sessions": 0,
            "created_channels": 0,
            "warnings_issued": 0,
            "bans_issued": 0,
            "kicks_issued": 0
        }
    return server_analytics[guild_id]

def update_server_analytics(guild_id: int, metric: str, value: int = 1):
    """Update server analytics"""
    analytics = get_server_analytics(guild_id)
    if metric in analytics:
        if isinstance(analytics[metric], int):
            analytics[metric] += value
        elif isinstance(analytics[metric], set):
            analytics[metric].add(value)

def get_top_users(guild_id: int, stat: str = "commands_used", limit: int = 10) -> List[Dict[str, Any]]:
    """Get top users by a specific statistic"""
    guild_users = []
    for user_id, stats in user_stats.items():
        if stat in stats:
            guild_users.append({
                "user_id": user_id,
                "value": stats[stat],
                "stats": stats
            })
    
    return sorted(guild_users, key=lambda x: x["value"], reverse=True)[:limit]

def clear_guild_data(guild_id: int):
    """Clear all data for a guild"""
    if guild_id in guild_settings:
        del guild_settings[guild_id]
    if guild_id in moderation_logs:
        del moderation_logs[guild_id]
    if guild_id in server_analytics:
        del server_analytics[guild_id]
    print(f"🗑️ Cleared all data for guild {guild_id}")

def backup_data() -> Dict[str, Any]:
    """Create a backup of all data"""
    backup = {
        "guild_settings": guild_settings,
        "user_stats": {str(k): v for k, v in user_stats.items()},
        "moderation_logs": {str(k): v for k, v in moderation_logs.items()},
        "server_analytics": {str(k): v for k, v in server_analytics.items()},
        "timestamp": datetime.datetime.now().isoformat()
    }
    print("💾 Data backup created")
    return backup

def restore_data(backup_data: Dict[str, Any]):
    """Restore data from backup"""
    global guild_settings, user_stats, moderation_logs, server_analytics
    
    if "guild_settings" in backup_data:
        guild_settings = backup_data["guild_settings"]
    if "user_stats" in backup_data:
        user_stats = {int(k): v for k, v in backup_data["user_stats"].items()}
    if "moderation_logs" in backup_data:
        moderation_logs = {int(k): v for k, v in backup_data["moderation_logs"].items()}
    if "server_analytics" in backup_data:
        server_analytics = {int(k): v for k, v in backup_data["server_analytics"].items()}
    
    print("📂 Data restored from backup")

def get_database_stats() -> Dict[str, int]:
    """Get database statistics"""
    return {
        "total_guilds": len(guild_settings),
        "total_users": len(user_stats),
        "total_mod_logs": sum(len(logs) for logs in moderation_logs.values()),
        "total_analytics": len(server_analytics)
    }
