from discord.ext import commands
from handlers.admin_commands import setup_admin_commands
from handlers.moderation_commands import setup_moderation_commands
from handlers.info_commands import setup_info_commands
from handlers.fun_commands import setup_fun_commands

def setup_commands(bot):
    """Setup all command handlers with duplicate prevention"""
    try:
        # Clear existing commands to prevent duplicates
        bot.clear()

        # Setup commands in order
        setup_info_commands(bot)
        setup_admin_commands(bot)
        setup_moderation_commands(bot)
        setup_fun_commands(bot)

        print("✅ All commands registered successfully")
    except Exception as e:
        print(f"❌ Error setting up commands: {e}")
        raise