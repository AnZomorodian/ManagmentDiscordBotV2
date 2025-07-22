
import discord
import asyncio
import datetime
import random
from config.settings import BOT_ACTIVITIES, VOICE_SETTINGS, COLORS
from utils.database import load_guild_settings

def has_admin_permissions():
    """Check if user has administrator permissions"""
    from discord.ext import commands
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)

async def log_action(guild, message):
    """Log actions to designated log channel"""
    settings = load_guild_settings(guild.id)
    if settings["log_channel"]:
        try:
            log_channel = guild.get_channel(settings["log_channel"])
            if log_channel:
                embed = discord.Embed(
                    description=message,
                    color=COLORS["info"],
                    timestamp=datetime.datetime.now()
                )
                await log_channel.send(embed=embed)
        except Exception:
            pass

async def setup_bot_status(bot):
    """Setup rotating bot status"""
    async def status_rotation():
        while True:
            for activity_config in BOT_ACTIVITIES:
                activity_type = getattr(discord.ActivityType, activity_config["type"])
                activity = discord.Activity(type=activity_type, name=activity_config["name"])
                await bot.change_presence(activity=activity, status=discord.Status.online)
                await asyncio.sleep(30)
    
    @bot.event
    async def on_ready():
        print(f'🚀 AMAZING MANAGEMENT BOT v3.0 - ONLINE!')
        print(f'🤖 Logged in as {bot.user} (ID: {bot.user.id})')
        print(f'🌐 Managing {len(bot.guilds)} servers')
        print(f'👥 Serving {sum(guild.member_count for guild in bot.guilds)} users')
        print(f'⚡ Bot latency: {round(bot.latency * 1000)}ms')
        print(f'📁 Modular architecture: ✅ Active')
        print('-' * 60)
        
        bot.loop.create_task(status_rotation())

def get_optimal_bitrate(guild):
    """Get optimal bitrate based on server boost level"""
    if guild.premium_tier >= 2:
        return VOICE_SETTINGS["VOICE_QUALITY_LEVELS"]["premium"]
    elif guild.premium_tier >= 1:
        return VOICE_SETTINGS["VOICE_QUALITY_LEVELS"]["high"]
    else:
        return VOICE_SETTINGS["VOICE_QUALITY_LEVELS"]["standard"]

def create_embed(title, description, color="info", **kwargs):
    """Create a standardized embed"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS.get(color, COLORS["info"]),
        timestamp=kwargs.get("timestamp", datetime.datetime.now())
    )
    
    if "thumbnail" in kwargs:
        embed.set_thumbnail(url=kwargs["thumbnail"])
    if "image" in kwargs:
        embed.set_image(url=kwargs["image"])
    if "footer" in kwargs:
        embed.set_footer(text=kwargs["footer"])
    
    return embed

def get_channel_name(member):
    """Generate a creative channel name"""
    from config.settings import CHANNEL_NAMES
    template = random.choice(CHANNEL_NAMES)
    return template.format(member.display_name)

async def send_welcome_message(member):
    """Send welcome message to new member"""
    settings = load_guild_settings(member.guild.id)
    
    if not settings["welcome_message"] or not settings["welcome_channel"]:
        return
    
    try:
        channel = member.guild.get_channel(settings["welcome_channel"])
        if channel:
            embed = create_embed(
                title="🎉 Welcome to the Server!",
                description=f"Welcome {member.mention} to **{member.guild.name}**!\n\nYou are member #{member.guild.member_count}",
                color="success",
                thumbnail=member.display_avatar.url
            )
            embed.add_field(
                name="📋 Next Steps", 
                value="• Read the rules\n• Get your roles\n• Join voice channels for auto-rooms!\n• Use `!help` for bot commands", 
                inline=False
            )
            await channel.send(embed=embed)
    except Exception:
        pass

async def assign_auto_role(member):
    """Assign auto-role to new member"""
    settings = load_guild_settings(member.guild.id)
    
    if settings["auto_role"]:
        try:
            role = member.guild.get_role(settings["auto_role"])
            if role:
                await member.add_roles(role, reason="Auto-role assignment")
                await log_action(member.guild, f"👤 Auto-role {role.mention} assigned to {member.mention}")
        except discord.Forbidden:
            pass
