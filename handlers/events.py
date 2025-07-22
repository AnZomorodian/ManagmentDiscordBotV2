
import discord
import asyncio
import datetime
import random
from utils.database import created_channels, load_guild_settings, get_user_stats
from utils.helpers import log_action, get_optimal_bitrate, get_channel_name, send_welcome_message, assign_auto_role
from config.settings import VOICE_SETTINGS

def setup_events(bot):
    """Setup all event handlers"""
    
    @bot.event
    async def on_voice_state_update(member, before, after):
        """Enhanced voice state update handler"""
        if member.bot:
            return
        
        guild_config = load_guild_settings(member.guild.id)
        if not guild_config["auto_voice"]:
            return
        
        # Check if joining a trigger channel
        if after.channel and not before.channel:
            if guild_config["trigger_channels"] and after.channel.id not in guild_config["trigger_channels"]:
                return
        
        # Track user stats
        user_stats = get_user_stats(member.id)
        
        # Check user limit
        user_channels = [ch for ch in created_channels.values() if ch["creator"] == member.id]
        if len(user_channels) >= guild_config["max_channels_per_user"]:
            return
        
        if after.channel and not before.channel:
            await create_voice_channel(member, after.channel, guild_config)

    @bot.event
    async def on_member_join(member):
        """Handle new member join"""
        # Assign auto-role
        await assign_auto_role(member)
        
        # Send welcome message
        await send_welcome_message(member)
        
        # Log member join
        await log_action(member.guild, f"👋 {member.mention} joined the server (Member #{member.guild.member_count})")

    @bot.event
    async def on_member_remove(member):
        """Handle member leave"""
        await log_action(member.guild, f"👋 {member.mention} left the server")

    @bot.event
    async def on_command_error(ctx, error):
        """Enhanced error handling"""
        from discord.ext import commands
        from utils.helpers import create_embed
        
        if isinstance(error, commands.CheckFailure):
            embed = create_embed(
                title="⛔ Access Denied",
                description="You need **Administrator** permissions to use this command!",
                color="error"
            )
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.CommandNotFound):
            embed = create_embed(
                title="❓ Command Not Found",
                description="Unknown command! Type `!help` to see available commands.",
                color="warning"
            )
            await ctx.send(embed=embed, delete_after=8)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = create_embed(
                title="❌ Missing Arguments",
                description="Missing required arguments for this command. Type `!help` for usage.",
                color="error"
            )
            await ctx.send(embed=embed, delete_after=10)
        else:
            print(f"⚠️ Unhandled error: {error}")

async def create_voice_channel(member, trigger_channel, guild_config):
    """Create a new voice channel for the member"""
    try:
        guild = member.guild
        category = trigger_channel.category
        
        # Get optimal bitrate based on server boost level
        bitrate = get_optimal_bitrate(guild)
        
        # Create the channel with enhanced settings
        new_channel = await guild.create_voice_channel(
            name=get_channel_name(member),
            category=category,
            user_limit=VOICE_SETTINGS["DEFAULT_USER_LIMIT"],
            bitrate=bitrate,  # Fixed: Using correct max bitrate
            reason=f"Auto-created for {member.display_name}"
        )
        
        # Store enhanced channel info
        created_channels[new_channel.id] = {
            "creator": member.id,
            "created_at": datetime.datetime.now(),
            "guild_id": guild.id,
            "original_channel": trigger_channel.id,
            "bitrate": bitrate,
            "user_limit": VOICE_SETTINGS["DEFAULT_USER_LIMIT"]
        }
        
        # Move member to new channel
        await member.move_to(new_channel)
        
        # Update user stats
        user_stats = get_user_stats(member.id)
        user_stats["channels_created"] += 1
        user_stats["last_active"] = datetime.datetime.now()
        
        # Log channel creation
        await log_action(guild, f"🎵 Voice channel created: **{new_channel.name}** by {member.mention} ({bitrate//1000}kbps)")
        
        print(f"✅ Created voice channel '{new_channel.name}' for {member.display_name} in {guild.name} ({bitrate//1000}kbps)")
        
        # Start advanced channel manager
        asyncio.create_task(advanced_channel_manager(new_channel))
        
    except discord.Forbidden:
        print(f"❌ Missing permissions to create voice channel for {member.display_name}")
    except Exception as e:
        print(f"⚠️ Error creating voice channel: {e}")

async def advanced_channel_manager(channel):
    """Advanced channel management with auto-deletion and activity tracking"""
    check_interval = VOICE_SETTINGS["CHANNEL_CHECK_INTERVAL"]
    empty_time = 0
    max_empty_time = VOICE_SETTINGS["AUTO_DELETE_TIMEOUT"]
    
    while True:
        await asyncio.sleep(check_interval)
        try:
            # Refresh channel object
            from main import bot
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
