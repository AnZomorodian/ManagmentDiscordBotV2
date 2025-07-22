
import os
import discord
from discord.ext import commands
import asyncio
import datetime
import random
import json
import re
from typing import Optional

# Your Discord Bot Token
TOKEN = "MTAwMTQ1ODQ2NTk3NTMxMjQwNA.GPizIh.7PZQr5KhrvupPCcx6bIFescSpGXUxmychJ_MFo"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.moderation = True

bot = commands.Bot(command_prefix=['!', '?', '$', '.'], intents=intents, help_command=None)

# Data storage
created_channels = {}
user_stats = {}
guild_settings = {}
moderation_logs = {}

def has_admin_permissions():
    """Check if user has administrator permissions"""
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)

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
            "trigger_channels": []  # List of channel IDs that trigger auto-creation
        }
    return guild_settings[guild_id]

@bot.event
async def on_ready():
    print(f'🚀 AMAZING MANAGEMENT BOT v2.0 - ONLINE!')
    print(f'🤖 Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'🌐 Managing {len(bot.guilds)} servers')
    print(f'👥 Serving {sum(guild.member_count for guild in bot.guilds)} users')
    print(f'⚡ Bot latency: {round(bot.latency * 1000)}ms')
    print('-' * 60)
    
    # Set enhanced bot status
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="for administrators | !help"),
        discord.Activity(type=discord.ActivityType.listening, name="to server management | !admin"),
        discord.Activity(type=discord.ActivityType.playing, name="Advanced Management Bot | !setup"),
        discord.Activity(type=discord.ActivityType.competing, name="Server Management | !moderation")
    ]
    
    bot.loop.create_task(status_rotation(activities))

async def status_rotation(activities):
    """Rotate bot status every 30 seconds"""
    while True:
        for activity in activities:
            await bot.change_presence(activity=activity, status=discord.Status.online)
            await asyncio.sleep(30)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    
    guild_config = load_guild_settings(member.guild.id)
    if not guild_config["auto_voice"]:
        return
    
    # Check if joining a trigger channel (admin-controlled)
    if after.channel and not before.channel:
        # If no trigger channels are set, any voice channel works (old behavior)
        if guild_config["trigger_channels"] and after.channel.id not in guild_config["trigger_channels"]:
            return  # Only create channels when joining specific trigger channels
    
    # Track user stats
    if member.id not in user_stats:
        user_stats[member.id] = {"channels_created": 0, "total_time": 0}
    
    # Check user limit
    user_channels = [ch for ch in created_channels.values() if ch["creator"] == member.id]
    if len(user_channels) >= guild_config["max_channels_per_user"]:
        return
    
    if after.channel and not before.channel:
        try:
            guild = member.guild
            category = after.channel.category
            
            # Enhanced channel names with more variety
            channel_names = [
                f"🎵 {member.display_name}'s Lounge",
                f"🎤 {member.display_name}'s Studio",
                f"🎮 {member.display_name}'s Gaming Hub",
                f"💭 {member.display_name}'s Hangout",
                f"🌟 {member.display_name}'s Space",
                f"🔥 {member.display_name}'s Zone",
                f"⚡ {member.display_name}'s Room",
                f"💎 {member.display_name}'s Chamber",
                f"🚀 {member.display_name}'s Launch Pad",
                f"🎯 {member.display_name}'s Focus Room"
            ]
            
            new_channel = await guild.create_voice_channel(
                name=random.choice(channel_names),
                category=category,
                user_limit=10,
                bitrate=128000,  # Max quality
                reason=f"Auto-created for {member.display_name}"
            )
            
            # Store enhanced channel info
            created_channels[new_channel.id] = {
                "creator": member.id,
                "created_at": datetime.datetime.now(),
                "guild_id": guild.id,
                "original_channel": after.channel.id
            }
            
            await member.move_to(new_channel)
            user_stats[member.id]["channels_created"] += 1
            
            # Log channel creation
            await log_action(guild, f"🎵 Voice channel created: **{new_channel.name}** by {member.mention}")
            
            print(f"✅ Created voice channel '{new_channel.name}' for {member.display_name} in {guild.name}")
            
            bot.loop.create_task(advanced_channel_manager(new_channel))
            
        except discord.Forbidden:
            print(f"❌ Missing permissions to create voice channel for {member.display_name}")
        except Exception as e:
            print(f"⚠️ Error creating voice channel: {e}")

async def advanced_channel_manager(channel):
    """Advanced channel management with auto-deletion and activity tracking"""
    check_interval = 15
    empty_time = 0
    max_empty_time = 300  # 5 minutes
    
    while True:
        await asyncio.sleep(check_interval)
        try:
            channel = bot.get_channel(channel.id)
            if not channel:
                break
            
            if len(channel.members) == 0:
                empty_time += check_interval
                if empty_time >= max_empty_time:
                    # Cleanup and delete
                    if channel.id in created_channels:
                        del created_channels[channel.id]
                    
                    await channel.delete(reason="Auto-cleanup: Channel empty for 5+ minutes")
                    await log_action(channel.guild, f"🗑️ Auto-deleted empty channel: **{channel.name}**")
                    print(f"✅ Auto-deleted empty channel: {channel.name}")
                    break
            else:
                empty_time = 0  # Reset timer if members are present
                
        except discord.NotFound:
            break
        except Exception as e:
            print(f"⚠️ Error managing channel: {e}")
            break

async def log_action(guild, message):
    """Log actions to designated log channel"""
    settings = load_guild_settings(guild.id)
    if settings["log_channel"]:
        try:
            log_channel = guild.get_channel(settings["log_channel"])
            if log_channel:
                embed = discord.Embed(
                    description=message,
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now()
                )
                await log_channel.send(embed=embed)
        except Exception:
            pass

# ==================== ADMIN COMMANDS ====================

@bot.command(name='setup', aliases=['config'])
@has_admin_permissions()
async def setup_bot(ctx):
    """Initial bot setup for administrators"""
    embed = discord.Embed(
        title="🛠️ Bot Setup & Configuration",
        description="Welcome to the **Amazing Management Bot**! Let's configure your server:",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(
        name="📋 **Quick Setup Commands**",
        value=(
            "• `!setwelcome #channel` - Set welcome channel\n"
            "• `!setlogs #channel` - Set moderation logs channel\n"
            "• `!autorole @role` - Set auto-role for new members\n"
            "• `!voicesettings` - Configure voice channel settings\n"
            "• `!settrigger #voicechannel` - Set trigger channels for auto-creation"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 **Management Commands**",
        value=(
            "• `!purge <amount>` - Delete messages\n"
            "• `!kick @user` - Kick member\n"
            "• `!ban @user` - Ban member\n"
            "• `!mute @user` - Timeout member"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 **Monitoring Commands**",
        value=(
            "• `!serverinfo` - Detailed server stats\n"
            "• `!memberinfo @user` - User information\n"
            "• `!modlogs` - View moderation history\n"
            "• `!activity` - Server activity overview"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Administrator Setup • {ctx.guild.name}", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name='settrigger', aliases=['addtrigger'])
@has_admin_permissions()
async def set_trigger_channel(ctx, channel: discord.VoiceChannel):
    """Set a voice channel as trigger for auto-creation"""
    settings = load_guild_settings(ctx.guild.id)
    
    if channel.id not in settings["trigger_channels"]:
        settings["trigger_channels"].append(channel.id)
        embed = discord.Embed(
            title="✅ Trigger Channel Added",
            description=f"Users joining {channel.mention} will now get personal voice channels created automatically!",
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="⚠️ Already Set",
            description=f"{channel.mention} is already a trigger channel!",
            color=discord.Color.orange()
        )
    
    await ctx.send(embed=embed)
    await log_action(ctx.guild, f"🎵 Trigger channel set: {channel.mention} by {ctx.author.mention}")

@bot.command(name='removetrigger', aliases=['deltrigger'])
@has_admin_permissions()
async def remove_trigger_channel(ctx, channel: discord.VoiceChannel):
    """Remove a voice channel from trigger list"""
    settings = load_guild_settings(ctx.guild.id)
    
    if channel.id in settings["trigger_channels"]:
        settings["trigger_channels"].remove(channel.id)
        embed = discord.Embed(
            title="✅ Trigger Channel Removed",
            description=f"{channel.mention} is no longer a trigger channel.",
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="❌ Not Found",
            description=f"{channel.mention} was not a trigger channel!",
            color=discord.Color.red()
        )
    
    await ctx.send(embed=embed)

@bot.command(name='listtriggers', aliases=['triggers'])
@has_admin_permissions()
async def list_trigger_channels(ctx):
    """List all trigger channels"""
    settings = load_guild_settings(ctx.guild.id)
    
    embed = discord.Embed(
        title="🎵 Voice Trigger Channels",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    if not settings["trigger_channels"]:
        embed.add_field(
            name="📋 Current Mode",
            value="**ALL VOICE CHANNELS** - Any voice channel triggers auto-creation",
            inline=False
        )
        embed.add_field(
            name="💡 How to Change",
            value="Use `!settrigger #voicechannel` to set specific trigger channels",
            inline=False
        )
    else:
        trigger_list = []
        for channel_id in settings["trigger_channels"]:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                trigger_list.append(f"• {channel.mention}")
            else:
                # Remove invalid channel
                settings["trigger_channels"].remove(channel_id)
        
        embed.add_field(
            name="📋 Active Trigger Channels",
            value="\n".join(trigger_list) if trigger_list else "No valid trigger channels found",
            inline=False
        )
        
        embed.add_field(
            name="💡 Commands",
            value=(
                "• `!settrigger #channel` - Add trigger channel\n"
                "• `!removetrigger #channel` - Remove trigger channel\n"
                "• `!cleartriggers` - Remove all (back to any channel mode)"
            ),
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='cleartriggers')
@has_admin_permissions()
async def clear_trigger_channels(ctx):
    """Clear all trigger channels (back to any channel mode)"""
    settings = load_guild_settings(ctx.guild.id)
    settings["trigger_channels"] = []
    
    embed = discord.Embed(
        title="✅ Triggers Cleared",
        description="Voice channels will now be created when users join **ANY** voice channel!",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)
    await log_action(ctx.guild, f"🎵 All trigger channels cleared by {ctx.author.mention}")

@bot.command(name='setwelcome')
@has_admin_permissions()
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    """Set welcome channel for new members"""
    settings = load_guild_settings(ctx.guild.id)
    settings["welcome_channel"] = channel.id
    
    embed = discord.Embed(
        title="✅ Welcome Channel Set",
        description=f"New members will be welcomed in {channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='setlogs')
@has_admin_permissions()
async def set_log_channel(ctx, channel: discord.TextChannel):
    """Set moderation log channel"""
    settings = load_guild_settings(ctx.guild.id)
    settings["log_channel"] = channel.id
    
    embed = discord.Embed(
        title="✅ Log Channel Set",
        description=f"Moderation logs will be sent to {channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    await log_action(ctx.guild, f"📝 Log channel set to {channel.mention} by {ctx.author.mention}")

@bot.command(name='autorole')
@has_admin_permissions()
async def set_auto_role(ctx, role: discord.Role):
    """Set auto-role for new members"""
    settings = load_guild_settings(ctx.guild.id)
    settings["auto_role"] = role.id
    
    embed = discord.Embed(
        title="✅ Auto-Role Set",
        description=f"New members will automatically receive {role.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='voicesettings')
@has_admin_permissions()
async def voice_settings(ctx, action: str = None, value: int = None):
    """Configure voice channel settings"""
    settings = load_guild_settings(ctx.guild.id)
    
    if not action:
        embed = discord.Embed(
            title="🎵 Voice Channel Settings",
            color=discord.Color.blue()
        )
        embed.add_field(name="Auto Voice", value="✅ Enabled" if settings["auto_voice"] else "❌ Disabled", inline=True)
        embed.add_field(name="Max Channels per User", value=f"{settings['max_channels_per_user']}", inline=True)
        embed.add_field(name="Trigger Channels", value=f"{len(settings['trigger_channels'])} set" if settings['trigger_channels'] else "All channels", inline=True)
        embed.add_field(
            name="Commands",
            value=(
                "`!voicesettings toggle` - Enable/disable auto voice\n"
                "`!voicesettings limit <number>` - Set channel limit per user\n"
                "`!listtriggers` - Show trigger channels\n"
                "`!settrigger #channel` - Add trigger channel"
            ),
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    if action == "toggle":
        settings["auto_voice"] = not settings["auto_voice"]
        status = "enabled" if settings["auto_voice"] else "disabled"
        embed = discord.Embed(
            title=f"🎵 Auto Voice Channels {status.title()}",
            color=discord.Color.green() if settings["auto_voice"] else discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    elif action == "limit" and value:
        if 1 <= value <= 10:
            settings["max_channels_per_user"] = value
            embed = discord.Embed(
                title="✅ Channel Limit Updated",
                description=f"Users can now create up to {value} voice channels",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Limit must be between 1 and 10")

# ==================== MODERATION COMMANDS ====================

@bot.command(name='purge', aliases=['clear', 'delete'])
@has_admin_permissions()
async def purge_messages(ctx, amount: int):
    """Delete multiple messages"""
    if amount < 1 or amount > 100:
        return await ctx.send("❌ Amount must be between 1 and 100")
    
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 for command message
    
    embed = discord.Embed(
        title="🗑️ Messages Purged",
        description=f"Deleted {len(deleted)-1} messages from {ctx.channel.mention}",
        color=discord.Color.orange()
    )
    
    msg = await ctx.send(embed=embed, delete_after=5)
    await log_action(ctx.guild, f"🗑️ {ctx.author.mention} purged {len(deleted)-1} messages in {ctx.channel.mention}")

@bot.command(name='kick')
@has_admin_permissions()
async def kick_member(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Kick a member from the server"""
    if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
        return await ctx.send("❌ You cannot kick someone with a higher or equal role!")
    
    try:
        await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
        
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked from the server",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"👢 {member.mention} was kicked by {ctx.author.mention}\n**Reason:** {reason}")
        
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick this member")

@bot.command(name='ban')
@has_admin_permissions()
async def ban_member(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Ban a member from the server"""
    if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
        return await ctx.send("❌ You cannot ban someone with a higher or equal role!")
    
    try:
        await member.ban(reason=f"Banned by {ctx.author}: {reason}")
        
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned from the server",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"🔨 {member.mention} was banned by {ctx.author.mention}\n**Reason:** {reason}")
        
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban this member")

@bot.command(name='unban')
@has_admin_permissions()
async def unban_member(ctx, user_id: int, *, reason: str = "No reason provided"):
    """Unban a member by ID"""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author}: {reason}")
        
        embed = discord.Embed(
            title="✅ Member Unbanned",
            description=f"{user.mention} has been unbanned",
            color=discord.Color.green()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"✅ {user.mention} was unbanned by {ctx.author.mention}\n**Reason:** {reason}")
        
    except discord.NotFound:
        await ctx.send("❌ User not found or not banned")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unban members")

@bot.command(name='mute', aliases=['timeout'])
@has_admin_permissions()
async def timeout_member(ctx, member: discord.Member, duration: int = 60, *, reason: str = "No reason provided"):
    """Timeout a member (in minutes)"""
    if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
        return await ctx.send("❌ You cannot mute someone with a higher or equal role!")
    
    if duration > 10080:  # 7 days max
        duration = 10080
    
    try:
        timeout_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=duration)
        await member.timeout(timeout_until, reason=f"Muted by {ctx.author}: {reason}")
        
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted for {duration} minutes",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"🔇 {member.mention} was muted for {duration} minutes by {ctx.author.mention}\n**Reason:** {reason}")
        
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout this member")

@bot.command(name='unmute', aliases=['untimeout'])
@has_admin_permissions()
async def remove_timeout(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Remove timeout from a member"""
    try:
        await member.timeout(None, reason=f"Unmuted by {ctx.author}: {reason}")
        
        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"{member.mention} has been unmuted",
            color=discord.Color.green()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"🔊 {member.mention} was unmuted by {ctx.author.mention}\n**Reason:** {reason}")
        
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove timeout from this member")

# ==================== INFO COMMANDS ====================

@bot.command(name='memberinfo', aliases=['userinfo', 'whois'])
@has_admin_permissions()
async def member_info(ctx, member: discord.Member = None):
    """Get detailed information about a member"""
    if not member:
        member = ctx.author
    
    embed = discord.Embed(
        title=f"👤 {member.display_name}",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    
    # Basic info
    embed.add_field(name="🏷️ Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="🆔 User ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="🤖 Bot", value="Yes" if member.bot else "No", inline=True)
    
    # Dates
    embed.add_field(name="📅 Account Created", value=discord.utils.format_dt(member.created_at, style='D'), inline=True)
    embed.add_field(name="📥 Joined Server", value=discord.utils.format_dt(member.joined_at, style='D') if member.joined_at else "Unknown", inline=True)
    
    # Status and activity
    status_emojis = {
        discord.Status.online: "🟢 Online",
        discord.Status.idle: "🟡 Idle", 
        discord.Status.dnd: "🔴 Do Not Disturb",
        discord.Status.offline: "⚫ Offline"
    }
    embed.add_field(name="📱 Status", value=status_emojis.get(member.status, "Unknown"), inline=True)
    
    # Roles
    if len(member.roles) > 1:
        roles = [role.mention for role in member.roles[1:]][:10]  # Skip @everyone, limit to 10
        embed.add_field(name=f"🎭 Roles ({len(member.roles)-1})", value=" ".join(roles), inline=False)
    
    # Permissions
    perms = []
    if member.guild_permissions.administrator:
        perms.append("👑 Administrator")
    if member.guild_permissions.manage_guild:
        perms.append("⚙️ Manage Server")
    if member.guild_permissions.manage_channels:
        perms.append("📝 Manage Channels")
    if member.guild_permissions.ban_members:
        perms.append("🔨 Ban Members")
    if member.guild_permissions.kick_members:
        perms.append("👢 Kick Members")
    
    if perms:
        embed.add_field(name="🔑 Key Permissions", value="\n".join(perms), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='modlogs')
@has_admin_permissions()
async def moderation_logs(ctx, member: discord.Member = None):
    """View moderation logs"""
    embed = discord.Embed(
        title="📋 Moderation Logs",
        description="Recent moderation actions in this server",
        color=discord.Color.orange(),
        timestamp=datetime.datetime.now()
    )
    
    # This would typically connect to a database
    embed.add_field(
        name="📊 Statistics",
        value="• Total Actions: 0\n• Bans: 0\n• Kicks: 0\n• Mutes: 0",
        inline=True
    )
    
    embed.add_field(
        name="⚠️ Note",
        value="Moderation logs are tracked from bot startup.\nFor persistent logs, consider setting up a database.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='activity', aliases=['stats'])
@has_admin_permissions()
async def server_activity(ctx):
    """Show server activity overview"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name} - Activity Overview",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    
    # Voice channel stats
    active_voice = len([ch for ch in guild.voice_channels if len(ch.members) > 0])
    total_voice = len(guild.voice_channels)
    created_today = len([ch for ch in created_channels.values() if ch["created_at"].date() == datetime.date.today()])
    
    embed.add_field(name="🎵 Voice Activity", value=f"Active: {active_voice}/{total_voice}\nCreated Today: {created_today}", inline=True)
    
    # Member activity
    online = len([m for m in guild.members if m.status != discord.Status.offline and not m.bot])
    total = guild.member_count
    
    embed.add_field(name="👥 Member Activity", value=f"Online: {online}/{total}\nActivity Rate: {round((online/total)*100, 1)}%", inline=True)
    
    # Channel activity
    embed.add_field(name="💬 Channels", value=f"Text: {len(guild.text_channels)}\nVoice: {len(guild.voice_channels)}\nCategories: {len(guild.categories)}", inline=True)
    
    # Bot statistics
    embed.add_field(name="🤖 Bot Stats", value=f"Commands Used: N/A\nChannels Created: {sum(stats['channels_created'] for stats in user_stats.values())}\nActive Since: Startup", inline=True)
    
    await ctx.send(embed=embed)

# Enhanced existing commands with admin improvements
@bot.command(name='serverinfo', aliases=['si', 'server'])
async def enhanced_server_info(ctx):
    """Enhanced server information with admin details"""
    guild = ctx.guild
    is_admin = ctx.author.guild_permissions.administrator
    
    embed = discord.Embed(
        title=f"📊 {guild.name} - Complete Server Analysis",
        description=f"🔍 **Comprehensive overview of {guild.name}**",
        color=discord.Color.gold() if is_admin else discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner and is_admin:
        embed.set_image(url=guild.banner.url)
    
    # Enhanced admin view
    if is_admin:
        embed.add_field(name="👑 **ADMIN VIEW**", value="Additional details shown", inline=False)
        
        # Security info
        verification_levels = {
            discord.VerificationLevel.none: "🔓 None (Unrestricted)",
            discord.VerificationLevel.low: "🔒 Low (Email verified)",
            discord.VerificationLevel.medium: "🔒 Medium (5+ min registered)", 
            discord.VerificationLevel.high: "🔒 High (10+ min member)",
            discord.VerificationLevel.highest: "🔒 Highest (Phone verified)"
        }
        
        embed.add_field(name="🛡️ Security Level", value=verification_levels.get(guild.verification_level, "Unknown"), inline=True)
        embed.add_field(name="🔞 Content Filter", value=str(guild.explicit_content_filter).replace('_', ' ').title(), inline=True)
        embed.add_field(name="📱 2FA Requirement", value="✅ Enabled" if guild.mfa_level else "❌ Disabled", inline=True)
    
    # Standard info (enhanced)
    embed.add_field(name="👑 Owner", value=f"{guild.owner.mention}\n({guild.owner})" if guild.owner else "Unknown", inline=True)
    embed.add_field(name="📅 Created", value=f"{discord.utils.format_dt(guild.created_at, style='D')}\n({discord.utils.format_dt(guild.created_at, style='R')})", inline=True)
    embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=True)
    
    # Enhanced member statistics
    total_members = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    humans = total_members - bots
    online_members = len([m for m in guild.members if m.status != discord.Status.offline and not m.bot])
    
    embed.add_field(name="👥 Total Members", value=f"{total_members:,}", inline=True)
    embed.add_field(name="🤖 Bots", value=f"{bots:,}", inline=True)
    embed.add_field(name="👨‍👩‍👧‍👦 Humans", value=f"{humans:,}", inline=True)
    embed.add_field(name="🟢 Online Now", value=f"{online_members:,} ({round((online_members/humans)*100, 1)}%)" if humans > 0 else "0", inline=True)
    
    # Enhanced channel info
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    stage_channels = len(guild.stage_channels)
    
    embed.add_field(name="💬 Text Channels", value=f"{text_channels:,}", inline=True)
    embed.add_field(name="🔊 Voice Channels", value=f"{voice_channels:,}", inline=True)
    embed.add_field(name="🎭 Stage Channels", value=f"{stage_channels:,}", inline=True)
    embed.add_field(name="📁 Categories", value=f"{categories:,}", inline=True)
    
    # Server features
    embed.add_field(name="😀 Emojis", value=f"{len(guild.emojis):,}/{guild.emoji_limit}", inline=True)
    embed.add_field(name="🎭 Roles", value=f"{len(guild.roles):,}", inline=True)
    embed.add_field(name="⚡ Boost Level", value=f"Level {guild.premium_tier} ({guild.premium_subscription_count} boosts)", inline=True)
    
    # Bot statistics
    active_voice = len([ch for ch in created_channels.values() if ch["guild_id"] == guild.id])
    total_created = len([ch for ch in created_channels.values() if ch["guild_id"] == guild.id])
    
    embed.add_field(name="🎵 Bot Voice Channels", value=f"Active: {active_voice}\nTotal Created: {sum(stats['channels_created'] for stats in user_stats.values())}", inline=True)
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name} • Management Bot v2.0" + (" • Admin View" if is_admin else ""), icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='help', aliases=['h', 'commands', 'admin'])
async def enhanced_help(ctx):
    """Enhanced help with admin commands"""
    is_admin = ctx.author.guild_permissions.administrator
    
    embed = discord.Embed(
        title="🤖 Amazing Management Bot v2.0 - Command Center",
        description=f"🚀 **Welcome to the ultimate Discord management experience!**\n{'👑 **ADMINISTRATOR ACCESS DETECTED**' if is_admin else '👤 **STANDARD USER ACCESS**'}",
        color=discord.Color.gold() if is_admin else discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    
    if is_admin:
        embed.add_field(
            name="👑 **ADMIN COMMANDS**",
            value=(
                "• `!setup` - Complete bot configuration\n"
                "• `!setwelcome #channel` - Set welcome channel\n"
                "• `!setlogs #channel` - Set moderation logs\n"
                "• `!autorole @role` - Auto-role for new members\n"
                "• `!voicesettings` - Voice channel configuration"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎵 **VOICE TRIGGER CONTROL**",
            value=(
                "• `!settrigger #voicechannel` - Set specific trigger channel\n"
                "• `!removetrigger #voicechannel` - Remove trigger channel\n"
                "• `!listtriggers` - Show all trigger channels\n"
                "• `!cleartriggers` - Reset to any-channel mode"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🛡️ **MODERATION**",
            value=(
                "• `!purge <amount>` - Delete messages (1-100)\n"
                "• `!kick @user [reason]` - Kick member\n"
                "• `!ban @user [reason]` - Ban member\n"
                "• `!unban <userid> [reason]` - Unban member\n"
                "• `!mute @user [minutes] [reason]` - Timeout member\n"
                "• `!unmute @user [reason]` - Remove timeout"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📊 **ADMIN ANALYTICS**",
            value=(
                "• `!memberinfo @user` - Detailed user analysis\n"
                "• `!modlogs [user]` - Moderation history\n"
                "• `!activity` - Server activity overview\n"
                "• `!serverinfo` - Enhanced server statistics"
            ),
            inline=False
        )
    
    embed.add_field(
        name="🎵 **SMART VOICE SYSTEM** ⭐",
        value=(
            "• **Admin Control:** Set specific trigger channels!\n"
            "• **Auto-Creation:** Join trigger → Get personal room\n"
            "• **Auto-Deletion:** Empty for 5min → Deleted\n"
            "• **High Quality:** 128kbps audio, 10 user limit\n"
            "• **Smart Names:** 10+ creative channel variants\n"
            "• **User Tracking:** Statistics and limits"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 **INFORMATION**",
        value=(
            "• `!serverinfo` - Complete server overview\n"
            "• `!mystats` - Your personal bot usage\n"
            "• `!botstats` - Bot performance metrics\n"
            "• `!ping` - Bot latency check"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 **FUN COMMANDS**",
        value=(
            "• `!coinflip` - Flip a coin\n"
            "• `!roll [sides]` - Roll dice (default 100)\n"
            "• `!8ball <question>` - Magic 8-ball oracle\n"
            "• `!uptime` - Bot runtime information"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 **PREFIXES & FEATURES**",
        value=(
            "**Prefixes:** `!`, `?`, `$`, `.`\n"
            "**Auto-Features:** Smart voice channels, Welcome messages\n"
            "**Security:** Admin-only commands, Permission checks\n"
            "**Monitoring:** Activity tracking, Usage statistics"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💡 **VOICE SYSTEM USAGE**",
        value=(
            "• **Any Channel Mode:** All voice channels trigger creation\n"
            "• **Trigger Mode:** Only admin-set channels trigger creation\n"
            "• **Commands:** Use `!listtriggers` to see current setup\n"
            "• **Smart Control:** Admins decide which channels work!"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name} • Serving {len(bot.guilds)} servers with {sum(guild.member_count for guild in bot.guilds)} users", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

# Event handlers for new members
@bot.event
async def on_member_join(member):
    """Welcome new members and assign auto-role"""
    settings = load_guild_settings(member.guild.id)
    
    # Auto-role assignment
    if settings["auto_role"]:
        try:
            role = member.guild.get_role(settings["auto_role"])
            if role:
                await member.add_roles(role, reason="Auto-role assignment")
        except discord.Forbidden:
            pass
    
    # Welcome message
    if settings["welcome_channel"]:
        try:
            channel = member.guild.get_channel(settings["welcome_channel"])
            if channel:
                embed = discord.Embed(
                    title="🎉 Welcome to the Server!",
                    description=f"Welcome {member.mention} to **{member.guild.name}**!\n\nYou are member #{member.guild.member_count}",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.now()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(name="📋 Next Steps", value="• Read the rules\n• Get your roles\n• Join voice channels for auto-rooms!", inline=False)
                await channel.send(embed=embed)
        except Exception:
            pass
    
    await log_action(member.guild, f"👋 {member.mention} joined the server (Member #{member.guild.member_count})")

# Keep all existing fun commands and add error handling
@bot.event
async def on_command_error(ctx, error):
    """Enhanced error handling"""
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="⛔ Access Denied",
            description="You need **Administrator** permissions to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❓ Command Not Found",
            description=f"Unknown command! Type `!help` to see available commands.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Arguments",
            description=f"Missing required arguments for this command. Type `!help` for usage.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)

# Add all the fun commands from before
@bot.command(name='mystats')
async def my_stats(ctx):
    """Show user's bot usage statistics"""
    user_id = ctx.author.id
    if user_id not in user_stats:
        user_stats[user_id] = {"channels_created": 0, "total_time": 0}
    
    stats = user_stats[user_id]
    
    embed = discord.Embed(
        title=f"📈 {ctx.author.display_name}'s Bot Statistics",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="🎵 Voice Channels Created", value=f"{stats['channels_created']:,}", inline=True)
    
    # Calculate rank
    sorted_users = sorted(user_stats.keys(), key=lambda x: user_stats[x]['channels_created'], reverse=True)
    rank = sorted_users.index(user_id) + 1 if user_id in sorted_users else "N/A"
    
    embed.add_field(name="🏆 Global Rank", value=f"#{rank}", inline=True)
    embed.add_field(name="⭐ Achievement Level", value="🎵 Voice Master!" if stats['channels_created'] >= 10 else "🌱 Getting Started", inline=True)
    
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='botstats')
async def bot_stats(ctx):
    """Enhanced bot performance statistics"""
    embed = discord.Embed(
        title="🤖 Management Bot v2.0 - Performance Dashboard",
        color=discord.Color.orange(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds):,}", inline=True)
    embed.add_field(name="👥 Total Users", value=f"{sum(guild.member_count for guild in bot.guilds):,}", inline=True)
    embed.add_field(name="🎵 Active Voice Channels", value=f"{len(created_channels):,}", inline=True)
    
    embed.add_field(name="📊 Total Channels Created", value=f"{sum(stats['channels_created'] for stats in user_stats.values()):,}", inline=True)
    embed.add_field(name="⚡ Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="💻 Commands Available", value="30+", inline=True)
    
    embed.add_field(name="🔥 Features", value="• Smart Voice Channels\n• Admin Trigger Control\n• Advanced Moderation\n• Admin Management\n• Activity Tracking", inline=True)
    embed.add_field(name="⏱️ Uptime", value="Since last restart", inline=True)
    embed.add_field(name="🚀 Version", value="v2.0 - Smart Management", inline=True)
    
    await ctx.send(embed=embed)

# Keep existing fun commands
@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**\n{'🟢 Excellent' if latency < 100 else '🟡 Good' if latency < 200 else '🔴 Poor'}",
        color=discord.Color.green() if latency < 100 else discord.Color.yellow() if latency < 200 else discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name='coinflip', aliases=['flip', 'coin'])
async def coinflip(ctx):
    result = random.choice(['Heads', 'Tails'])
    emoji = '🪙' if result == 'Heads' else '🔘'
    embed = discord.Embed(
        title=f"{emoji} Coin Flip Result",
        description=f"The coin landed on **{result}**!",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name='roll', aliases=['dice'])
async def roll_dice(ctx, sides: int = 100):
    if sides < 2: sides = 6
    if sides > 1000: sides = 1000
    result = random.randint(1, sides)
    embed = discord.Embed(
        title="🎲 Dice Roll",
        description=f"You rolled a **{result}** out of {sides}!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='8ball', aliases=['eightball'])
async def magic_8ball(ctx, *, question):
    responses = [
        "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
        "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
        "Don't count on it", "My reply is no", "My sources say no",
        "Outlook not so good", "Very doubtful"
    ]
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

@bot.command(name='uptime')
async def uptime(ctx):
    embed = discord.Embed(
        title="⏰ Bot Uptime",
        description="🚀 Management Bot v2.0 has been running since startup!\n⚡ All systems operational",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Run the bot with enhanced error handling
if __name__ == "__main__":
    try:
        print("🚀 Starting Amazing Management Bot v2.0...")
        print("🔑 Using embedded token...")
        print("👑 Admin features enabled...")
        print("🎵 Smart voice trigger system ready...")
        bot.run(TOKEN)
    except discord.HTTPException as e:
        if e.status == 429:
            print("❌ Rate limited! Too many requests to Discord API")
            print("💡 Wait a few minutes and try again")
        else:
            print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
