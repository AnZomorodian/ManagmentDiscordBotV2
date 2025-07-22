import discord
import asyncio
import random
from config.settings import EMBED_COLORS, STATUS_MESSAGES, BOT_VERSION

def create_embed(title, description="", color="primary", thumbnail=None, footer=None):
    """Create a standardized embed with consistent styling"""
    try:
        # Get color value
        if isinstance(color, str):
            color_value = EMBED_COLORS.get(color, EMBED_COLORS['primary'])
        else:
            color_value = color

        embed = discord.Embed(
            title=title,
            description=description,
            color=color_value
        )

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if footer:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text=f"Amazing Bot v{BOT_VERSION}")

        return embed

    except Exception as e:
        print(f"Error creating embed: {e}")
        # Return basic embed as fallback
        return discord.Embed(
            title=title,
            description=description,
            color=0x0099ff
        )

async def setup_bot_status(bot):
    """Rotate bot status messages"""
    while not bot.is_closed():
        try:
            status_message = random.choice(STATUS_MESSAGES)
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=status_message
                ),
                status=discord.Status.online
            )
            await asyncio.sleep(300)  # Change every 5 minutes
        except Exception as e:
            print(f"Error updating status: {e}")
            await asyncio.sleep(60)

def validate_environment():
    """Validate environment variables"""
    import os
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        print("❌ DISCORD_TOKEN not found in .env file!")
        return False

    if len(token) < 50:
        print("❌ Invalid Discord token format!")
        return False

    print("✅ Token validation: ✅ Valid")
    return True

async def log_action(guild, action, details):
    """Log moderation actions"""
    try:
        print(f"🛡️ [MODERATION] {guild.name}: {action} - {details}")
    except Exception as e:
        print(f"Error logging action: {e}")

def format_time(seconds):
    """Format seconds into readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def get_member_status(member):
    """Get formatted member status"""
    status_emojis = {
        discord.Status.online: "🟢",
        discord.Status.idle: "🟡",
        discord.Status.dnd: "🔴",
        discord.Status.offline: "⚫"
    }
    return status_emojis.get(member.status, "⚫")

import os
import os.sys
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from config.settings import BOT_ACTIVITIES, VOICE_SETTINGS, COLORS

def has_admin_permissions():
    """Decorator to check if user has admin permissions"""
    def predicate(ctx):
        return (
            ctx.author.guild_permissions.administrator or
            ctx.author.guild_permissions.manage_guild or
            ctx.author.id == ctx.guild.owner_id
        )
    return commands.check(predicate)

def has_mod_permissions():
    """Decorator to check if user has moderation permissions"""
    def predicate(ctx):
        return (
            ctx.author.guild_permissions.kick_members or
            ctx.author.guild_permissions.ban_members or
            ctx.author.guild_permissions.manage_messages or
            ctx.author.guild_permissions.administrator
        )
    return commands.check(predicate)

async def safe_send(ctx, content=None, embed=None, delete_after=None):
    """Safely send messages with error handling"""
    try:
        return await ctx.send(content=content, embed=embed, delete_after=delete_after)
    except discord.Forbidden:
        try:
            await ctx.author.send("❌ I don't have permission to send messages in that channel!")
        except:
            pass
    except discord.HTTPException as e:
        print(f"❌ Failed to send message: {e}")
    except Exception as e:
        print(f"❌ Unexpected error sending message: {e}")

def get_member_info(member):
    """Get comprehensive member information"""
    return {
        "id": member.id,
        "name": str(member),
        "display_name": member.display_name,
        "joined_at": member.joined_at,
        "created_at": member.created_at,
        "roles": [role.name for role in member.roles if role.name != "@everyone"],
        "top_role": member.top_role.name if member.top_role.name != "@everyone" else "None",
        "permissions": [perm for perm, value in member.guild_permissions if value],
        "status": str(member.status),
        "activity": str(member.activity) if member.activity else "None"
    }

def check_bot_permissions(guild, permissions_list):
    """Check if bot has required permissions"""
    bot_member = guild.me
    missing_perms = []
    
    for perm in permissions_list:
        if not getattr(bot_member.guild_permissions, perm, False):
            missing_perms.append(perm.replace('_', ' ').title())
    
    return missing_perms

def get_environment_info():
    """Get environment information for debugging"""
    return {
        "token_configured": bool(os.getenv('DISCORD_TOKEN')),
        "env_file_exists": os.path.exists('.env'),
        "python_version": os.sys.version,
        "discord_py_version": discord.__version__
    }