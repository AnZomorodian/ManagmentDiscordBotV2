
import discord
from discord.ext import commands
import asyncio
import random
from config.settings import VOICE_SETTINGS, CHANNEL_NAMES, COLORS, DEFAULT_GUILD_SETTINGS
from utils.database import load_guild_settings, save_guild_settings
from utils.helpers import create_embed, log_action

def setup_events(bot):
    """Setup all event handlers with enhanced functionality"""
    
    @bot.event
    async def on_guild_join(guild):
        """Enhanced guild join event with .env awareness"""
        print(f"✅ Bot joined new guild: {guild.name} (ID: {guild.id})")
        print(f"👥 Members: {guild.member_count}")
        
        # Initialize guild settings
        settings = DEFAULT_GUILD_SETTINGS.copy()
        save_guild_settings(guild.id, settings)
        
        # Send welcome message to system channel
        if guild.system_channel:
            embed = create_embed(
                title="🎉 Thanks for adding Amazing Management Bot v3.1!",
                description=(
                    f"Hello **{guild.name}**! I'm ready to help manage your server.\n\n"
                    f"🔐 **Secure Configuration**: Using .env for token protection\n"
                    f"⚙️ **Quick Setup**: Use `!setup` to get started\n"
                    f"📚 **Help**: Use `!help` for command list\n\n"
                    f"**Key Features:**\n"
                    f"🎵 Auto Voice Channels\n"
                    f"🛡️ Advanced Moderation\n" 
                    f"📊 Statistics & Analytics\n"
                    f"🎪 Fun Commands & Games"
                ),
                color="success"
            )
            try:
                await guild.system_channel.send(embed=embed)
            except:
                pass

    @bot.event
    async def on_voice_state_update(member, before, after):
        """Enhanced voice state management with .env settings"""
        if member.bot:
            return
            
        guild_settings = load_guild_settings(member.guild.id)
        if not guild_settings.get("auto_voice", True):
            return
            
        trigger_channels = guild_settings.get("trigger_channels", [])
        max_channels = guild_settings.get("max_channels_per_user", 3)
        
        # User joined a trigger channel
        if after.channel and after.channel.id in trigger_channels:
            try:
                # Check user's current channel count
                user_channels = [
                    channel for channel in member.guild.voice_channels
                    if channel.name.startswith(member.display_name) or 
                       member.display_name in channel.name
                ]
                
                if len(user_channels) >= max_channels:
                    return
                
                # Create new voice channel
                channel_name = random.choice(CHANNEL_NAMES).format(member.display_name)
                voice_quality = guild_settings.get("voice_quality", "high")
                bitrate = VOICE_SETTINGS["VOICE_QUALITY_LEVELS"][voice_quality]
                
                new_channel = await member.guild.create_voice_channel(
                    name=channel_name,
                    category=after.channel.category,
                    bitrate=min(bitrate, member.guild.bitrate_limit),
                    user_limit=guild_settings.get("default_user_limit", 0)
                )
                
                # Move user to new channel
                await member.move_to(new_channel)
                
                # Set channel permissions
                await new_channel.set_permissions(
                    member, 
                    manage_channels=True,
                    manage_permissions=True,
                    mute_members=True,
                    deafen_members=True
                )
                
                print(f"🎵 Created voice channel '{channel_name}' for {member.display_name}")
                
                # Auto-delete setup
                asyncio.create_task(auto_delete_channel(new_channel, guild_settings))
                
            except Exception as e:
                print(f"❌ Error creating voice channel: {e}")

    async def auto_delete_channel(channel, guild_settings):
        """Auto-delete empty voice channels"""
        timeout = guild_settings.get("auto_delete_timeout", 300)
        
        while True:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            try:
                if len(channel.members) == 0:
                    await asyncio.sleep(timeout)  # Wait for timeout
                    if len(channel.members) == 0:  # Double check
                        await channel.delete(reason="Auto-delete: Channel empty")
                        print(f"🗑️ Auto-deleted empty voice channel: {channel.name}")
                        break
            except discord.NotFound:
                break  # Channel already deleted
            except Exception as e:
                print(f"❌ Error in auto-delete: {e}")
                break

    @bot.event
    async def on_member_join(member):
        """Enhanced member join event"""
        guild_settings = load_guild_settings(member.guild.id)
        
        # Welcome message
        welcome_channel_id = guild_settings.get("welcome_channel")
        if welcome_channel_id and guild_settings.get("welcome_message", True):
            welcome_channel = bot.get_channel(welcome_channel_id)
            if welcome_channel:
                embed = create_embed(
                    title=f"🎉 Welcome to {member.guild.name}!",
                    description=f"Hey {member.mention}! Welcome to our awesome community!",
                    color="success"
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                try:
                    await welcome_channel.send(embed=embed)
                except:
                    pass
        
        # Auto-role
        auto_role_id = guild_settings.get("auto_role")
        if auto_role_id:
            role = member.guild.get_role(auto_role_id)
            if role:
                try:
                    await member.add_roles(role, reason="Auto-role assignment")
                    print(f"✅ Added auto-role '{role.name}' to {member.display_name}")
                except Exception as e:
                    print(f"❌ Error adding auto-role: {e}")

    @bot.event
    async def on_command_error(ctx, error):
        """Enhanced error handling"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="❌ Missing Permissions",
                description="You don't have the required permissions to use this command!",
                color="error"
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = create_embed(
                title="❌ Bot Missing Permissions",
                description=f"I need these permissions: {', '.join(error.missing_permissions)}",
                color="error"
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = create_embed(
                title="⏰ Command Cooldown",
                description=f"Please wait {error.retry_after:.1f} seconds before using this command again.",
                color="warning"
            )
            await ctx.send(embed=embed)
        else:
            embed = create_embed(
                title="❌ An Error Occurred",
                description=f"```{str(error)[:1000]}```",
                color="error"
            )
            await ctx.send(embed=embed)
            print(f"❌ Command error: {error}")
