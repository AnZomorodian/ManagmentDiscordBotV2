
from discord.ext import commands
from handlers.admin_commands import setup_admin_commands
from handlers.moderation_commands import setup_moderation_commands
from handlers.info_commands import setup_info_commands
from handlers.fun_commands import setup_fun_commands

def setup_commands(bot):
    """Setup all command handlers with comprehensive error handling"""
    try:
        # Clear existing commands to prevent conflicts
        bot.clear()
        
        # Setup commands in order
        print("📊 Loading info commands...")
        setup_info_commands(bot)
        
        print("👑 Loading admin commands...")
        setup_admin_commands(bot)
        
        print("🛡️ Loading moderation commands...")
        setup_moderation_commands(bot)
        
        print("🎪 Loading fun commands...")
        setup_fun_commands(bot)

        print("✅ All commands registered successfully")
        print(f"📋 Total commands loaded: {len(bot.commands)}")
        
    except Exception as e:
        print(f"❌ Error setting up commands: {e}")
        raise
