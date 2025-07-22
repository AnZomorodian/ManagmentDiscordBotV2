
import discord
import asyncio
import datetime
import random
import os
from dotenv import load_dotenv
from config.settings import BOT_ACTIVITIES, VOICE_SETTINGS, COLORS
from utils.database import load_guild_settings

# Load environment variables
load_dotenv()

def create_embed(title, description, color="info", thumbnail=None, footer=None):
    """Create a standardized embed with enhanced styling"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS.get(color, COLORS["info"]),
        timestamp=datetime.datetime.utcnow()
    )
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if footer:
        embed.set_footer(text=footer)
    else:
        embed.set_footer(text="Amazing Management Bot v3.1 | Powered by .env security")
    
    return embed

def format_uptime(uptime_seconds):
    """Format uptime in a readable format"""
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    if days > 0:
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"
    elif hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(minutes)}m {int(seconds)}s"

def get_voice_quality_name(bitrate):
    """Get voice quality name based on bitrate"""
    for quality, rate in VOICE_SETTINGS["VOICE_QUALITY_LEVELS"].items():
        if bitrate <= rate:
            return quality.title()
    return "Premium+"

async def setup_bot_status(bot):
    """Setup rotating bot status with environment awareness"""
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            activity_data = random.choice(BOT_ACTIVITIES)
            activity_type = getattr(discord.ActivityType, activity_data["type"])
            activity_name = activity_data["name"]
            
            # Dynamic status with server count
            if "{}" in activity_name:
                activity_name = activity_name.format(len(bot.guilds))
            
            activity = discord.Activity(type=activity_type, name=activity_name)
            await bot.change_presence(
                status=discord.Status.online,
                activity=activity
            )
            
            await asyncio.sleep(300)  # Change every 5 minutes
            
        except Exception as e:
            print(f"❌ Status update error: {e}")
            await asyncio.sleep(60)  # Retry in 1 minute

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

def log_action(action, user, target=None, reason=None):
    """Log moderation actions"""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[{timestamp}] {action} by {user}"
    
    if target:
        log_entry += f" on {target}"
    if reason:
        log_entry += f" - Reason: {reason}"
    
    print(f"📝 {log_entry}")
    return log_entry

def validate_token():
    """Validate Discord token format"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        return False, "Token not found in environment variables"
    
    # Basic token format validation
    if len(token) < 50:
        return False, "Token appears to be too short"
    
    if not any(char.isdigit() for char in token):
        return False, "Token should contain numbers"
    
    return True, "Token format appears valid"

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
