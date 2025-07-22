from discord.ext import commands
from handlers.admin_commands import setup_admin_commands
from handlers.moderation_commands import setup_moderation_commands
from handlers.info_commands import setup_info_commands
from handlers.fun_commands import setup_fun_commands

def setup_commands(bot):
    """Setup all command categories"""
    setup_info_commands(bot)
    setup_admin_commands(bot)
    setup_moderation_commands(bot)
    setup_fun_commands(bot)
    print("📝 All command categories loaded")