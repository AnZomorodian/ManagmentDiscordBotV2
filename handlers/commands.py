
from discord.ext import commands
from handlers.admin_commands import setup_admin_commands
from handlers.moderation_commands import setup_moderation_commands
from handlers.info_commands import setup_info_commands
from handlers.fun_commands import setup_fun_commands

def setup_commands(bot):
    """Setup all command handlers with proper error handling"""
    try:
        # Remove existing commands if they exist
        if hasattr(bot, 'commands') and bot.commands:
            # Create a copy of commands to avoid modification during iteration
            commands_to_remove = list(bot.commands)
            for command in commands_to_remove:
                bot.remove_command(command.name)

        # Setup commands in order
        setup_info_commands(bot)
        setup_admin_commands(bot)
        setup_moderation_commands(bot)
        setup_fun_commands(bot)

        print("✅ All commands registered successfully")
        print(f"📋 Total commands loaded: {len(bot.commands)}")
        
    except Exception as e:
        print(f"❌ Error setting up commands: {e}")
        raise
