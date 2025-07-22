
import discord
import asyncio
import random
from utils.helpers import create_embed, log_action
from config.settings import CHANNEL_NAMES, VOICE_SETTINGS

# Store created channels and trigger channels
created_channels = {}
trigger_channels = set()

def setup_events(bot):
    """Setup all event handlers with enhanced functionality"""

    @bot.event
    async def on_member_join(member):
        """Welcome new members"""
        try:
            embed = create_embed(
                title="👋 Welcome!",
                description=f"Welcome to **{member.guild.name}**, {member.mention}!\n\nUse `!help` to see available commands.",
                color="success",
                thumbnail=member.display_avatar.url
            )
            
            # Try to find a welcome channel
            welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
            if not welcome_channel:
                welcome_channel = discord.utils.get(member.guild.text_channels, name='general')
            
            if welcome_channel:
                await welcome_channel.send(embed=embed)
                
        except Exception as e:
            print(f"Error in on_member_join: {e}")

    @bot.event
    async def on_member_remove(member):
        """Log member leaving"""
        try:
            print(f"👋 {member.display_name} left {member.guild.name}")
        except Exception as e:
            print(f"Error in on_member_remove: {e}")

    @bot.event
    async def on_voice_state_update(member, before, after):
        """Enhanced voice state management with proper trigger handling"""
        if member.bot:
            return
            
        try:
            # User joined a voice channel
            if after.channel and after.channel != before.channel:
                # Check if it's a trigger channel
                if after.channel.id in trigger_channels:
                    await handle_trigger_channel_join(member, after.channel)
                    
            # User left a voice channel
            if before.channel and before.channel != after.channel:
                await handle_channel_cleanup(before.channel)
                
        except Exception as e:
            print(f"Error in voice state update: {e}")

    async def handle_trigger_channel_join(member, trigger_channel):
        """Handle user joining a trigger channel"""
        try:
            # Check user's current channel count
            user_channels = [ch for ch in created_channels.values() if ch.get('owner_id') == member.id]
            if len(user_channels) >= VOICE_SETTINGS['max_user_channels']:
                embed = create_embed(
                    title="❌ Channel Limit Reached",
                    description=f"You can only have {VOICE_SETTINGS['max_user_channels']} voice channels at once!",
                    color="error"
                )
                try:
                    await member.send(embed=embed)
                except:
                    pass
                return

            # Create new voice channel
            channel_name = random.choice(CHANNEL_NAMES).format(member.display_name)
            
            new_channel = await member.guild.create_voice_channel(
                name=channel_name,
                category=trigger_channel.category,
                bitrate=VOICE_SETTINGS['default_bitrate'],
                user_limit=VOICE_SETTINGS['default_user_limit']
            )
            
            # Store channel info
            created_channels[new_channel.id] = {
                'owner_id': member.id,
                'created_at': discord.utils.utcnow(),
                'channel': new_channel
            }
            
            # Move user to new channel
            await member.move_to(new_channel)
            
            print(f"🎵 Created voice channel '{channel_name}' for {member.display_name}")
            
            # Setup auto-delete
            asyncio.create_task(auto_delete_channel(new_channel))
            
        except Exception as e:
            print(f"Error creating voice channel: {e}")

    async def handle_channel_cleanup(channel):
        """Clean up empty voice channels"""
        try:
            if channel.id in created_channels and len(channel.members) == 0:
                # Start cleanup timer
                asyncio.create_task(auto_delete_channel(channel))
        except Exception as e:
            print(f"Error in channel cleanup: {e}")

    async def auto_delete_channel(channel):
        """Auto-delete empty voice channels after timeout"""
        try:
            await asyncio.sleep(VOICE_SETTINGS['auto_delete_timeout'])
            
            # Check if channel still exists and is empty
            if channel.id in created_channels:
                try:
                    # Refresh channel to get current member count
                    updated_channel = bot.get_channel(channel.id)
                    if updated_channel and len(updated_channel.members) == 0:
                        await updated_channel.delete(reason="Auto-cleanup: Empty voice channel")
                        created_channels.pop(channel.id, None)
                        print(f"🗑️ Auto-deleted empty voice channel: {channel.name}")
                except discord.NotFound:
                    # Channel already deleted
                    created_channels.pop(channel.id, None)
                except Exception as e:
                    print(f"Error deleting channel: {e}")
                    
        except Exception as e:
            print(f"Error in auto_delete_channel: {e}")

    # Add command for setting trigger channels
    @bot.command(name='settrigger')
    @discord.ext.commands.has_permissions(manage_channels=True)
    async def set_trigger_channel(ctx, channel: discord.VoiceChannel = None):
        """Set or toggle a voice channel as trigger for auto-creation"""
        try:
            if not channel:
                embed = create_embed(
                    title="❌ Invalid Usage",
                    description="Please specify a voice channel!\n**Usage:** `!settrigger #voice-channel`",
                    color="error"
                )
                await ctx.send(embed=embed)
                return
            
            if channel.id in trigger_channels:
                # Remove from trigger channels
                trigger_channels.remove(channel.id)
                embed = create_embed(
                    title="🔄 Trigger Removed",
                    description=f"{channel.mention} is no longer a trigger channel.",
                    color="warning"
                )
            else:
                # Add to trigger channels
                trigger_channels.add(channel.id)
                embed = create_embed(
                    title="✅ Trigger Channel Set",
                    description=f"{channel.mention} is now a trigger channel!\n\n**How it works:**\n• Users joining this channel will get their own voice room\n• Rooms auto-delete when empty (5 min timeout)\n• Users can have max {VOICE_SETTINGS['max_user_channels']} rooms",
                    color="success"
                )
            
            await ctx.send(embed=embed)
            print(f"🎵 Trigger channel {'added' if channel.id in trigger_channels else 'removed'}: {channel.name}")
            
        except Exception as e:
            embed = create_embed(
                title="❌ Error",
                description=f"Failed to set trigger channel: {str(e)}",
                color="error"
            )
            await ctx.send(embed=embed)
            print(f"Error in settrigger command: {e}")

    @bot.command(name='triggerlist')
    @discord.ext.commands.has_permissions(manage_channels=True)
    async def list_trigger_channels(ctx):
        """List all trigger channels"""
        try:
            if not trigger_channels:
                embed = create_embed(
                    title="📋 Trigger Channels",
                    description="No trigger channels set.\nUse `!settrigger #channel` to add one.",
                    color="info"
                )
            else:
                channel_list = []
                for channel_id in trigger_channels:
                    channel = bot.get_channel(channel_id)
                    if channel:
                        channel_list.append(f"🎵 {channel.mention}")
                
                embed = create_embed(
                    title="📋 Active Trigger Channels",
                    description="\n".join(channel_list) if channel_list else "No valid trigger channels found.",
                    color="info"
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = create_embed(
                title="❌ Error",
                description=f"Failed to list trigger channels: {str(e)}",
                color="error"
            )
            await ctx.send(embed=embed)

    print("🎭 Event handlers loaded successfully")
