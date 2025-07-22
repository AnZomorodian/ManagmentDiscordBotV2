import discord
from discord.ext import commands
import asyncio
import random
from config.settings import VOICE_SETTINGS, CHANNEL_NAMES, COLORS, DEFAULT_GUILD_SETTINGS
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
            
        # User joined a trigger channel
        if after.channel and after.channel != before.channel:
            if after.channel:
                try:
                    # Create new voice channel
                    channel_name = random.choice(CHANNEL_NAMES).format(member.display_name)
                    new_channel = await member.guild.create_voice_channel(
                        name=channel_name,
                        category=after.channel.category,
                        bitrate=64000,
                        user_limit= 0
                    )
                    
                    # Move user to new channel
                    await member.move_to(new_channel)
                    
                    print(f"🎵 Created voice channel '{channel_name}' for {member.display_name}")
                    
                    # Auto-delete setup
                    asyncio.create_task(auto_delete_channel(new_channel))
                    
                except Exception as e:
                    print(f"❌ Error creating voice channel: {e}")

        # Handle leaving voice channels
        if before.channel:
            if before.channel and len(before.channel.members) == 0:
                try:
                    await before.channel.delete(reason="Auto-delete: Channel empty")
                    print(f"🗑️ Auto-deleted empty voice channel: {before.channel.name}")
                except Exception as e:
                    print(f"❌ Error deleting channel: {e}")

    async def auto_delete_channel(channel):
        """Auto-delete empty voice channels"""
        await asyncio.sleep(300)  # Wait for timeout
        
        try:
            if len(channel.members) == 0:
                await channel.delete(reason="Auto-delete: Channel empty")
                print(f"🗑️ Auto-deleted empty voice channel: {channel.name}")
        except discord.NotFound:
            pass  # Channel already deleted
        except Exception as e:
            print(f"❌ Error in auto-delete: {e}")

    @bot.event
    async def on_member_join(member):
        """Enhanced member join event"""
        
        # Welcome message
        if member.guild.system_channel:
            welcome_channel = member.guild.system_channel
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

    print("🎭 Event handlers loaded successfully")