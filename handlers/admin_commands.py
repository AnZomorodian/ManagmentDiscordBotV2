
import discord
import datetime
from discord.ext import commands
from utils.helpers import has_admin_permissions, log_action, create_embed
from utils.database import load_guild_settings
from config.settings import COLORS

def setup_admin_commands(bot):
    """Setup administrative commands"""
    
    @bot.command(name='setup', aliases=['config'])
    @has_admin_permissions()
    async def setup_bot(ctx):
        """Initial bot setup for administrators"""
        embed = create_embed(
            title="🛠️ Bot Setup & Configuration v3.0",
            description="Welcome to the **Amazing Management Bot**! Let's configure your server:",
            color="admin"
        )
        
        embed.add_field(
            name="📋 **Quick Setup Commands**",
            value=(
                "• `!setwelcome #channel` - Set welcome channel\n"
                "• `!setlogs #channel` - Set moderation logs channel\n"
                "• `!autorole @role` - Set auto-role for new members\n"
                "• `!voicesettings` - Configure voice channel settings\n"
                "• `!settrigger #voicechannel` - Set trigger channels"
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
            name="📊 **Enhanced Features**",
            value=(
                "• Modular architecture for better performance\n"
                "• Fixed voice channel bitrate issues\n"
                "• Enhanced error handling\n"
                "• Improved user statistics tracking"
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
            embed = create_embed(
                title="✅ Trigger Channel Added",
                description=f"Users joining {channel.mention} will now get personal voice channels created automatically!",
                color="success"
            )
        else:
            embed = create_embed(
                title="⚠️ Already Set",
                description=f"{channel.mention} is already a trigger channel!",
                color="warning"
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
            embed = create_embed(
                title="✅ Trigger Channel Removed",
                description=f"{channel.mention} is no longer a trigger channel.",
                color="success"
            )
        else:
            embed = create_embed(
                title="❌ Not Found",
                description=f"{channel.mention} was not a trigger channel!",
                color="error"
            )
        
        await ctx.send(embed=embed)

    @bot.command(name='voicesettings')
    @has_admin_permissions()
    async def voice_settings(ctx, action: str = None, value: int = None):
        """Configure voice channel settings"""
        settings = load_guild_settings(ctx.guild.id)
        
        if not action:
            embed = create_embed(
                title="🎵 Voice Channel Settings v3.0",
                description="Enhanced voice management system",
                color="voice"
            )
            embed.add_field(name="Auto Voice", value="✅ Enabled" if settings["auto_voice"] else "❌ Disabled", inline=True)
            embed.add_field(name="Max Channels per User", value=f"{settings['max_channels_per_user']}", inline=True)
            embed.add_field(name="Voice Quality", value=f"{settings['voice_quality'].title()}", inline=True)
            embed.add_field(
                name="🆕 New Features",
                value=(
                    "• Fixed bitrate compatibility\n"
                    "• Server boost optimization\n"
                    "• Enhanced channel names\n"
                    "• Better error handling"
                ),
                inline=False
            )
            await ctx.send(embed=embed)
            return
        
        if action == "toggle":
            settings["auto_voice"] = not settings["auto_voice"]
            status = "enabled" if settings["auto_voice"] else "disabled"
            embed = create_embed(
                title=f"🎵 Auto Voice Channels {status.title()}",
                description=f"Voice channel auto-creation is now **{status}**",
                color="success" if settings["auto_voice"] else "error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='setwelcome')
    @has_admin_permissions()
    async def set_welcome_channel(ctx, channel: discord.TextChannel):
        """Set welcome channel for new members"""
        settings = load_guild_settings(ctx.guild.id)
        settings["welcome_channel"] = channel.id
        
        embed = create_embed(
            title="✅ Welcome Channel Set",
            description=f"New members will be welcomed in {channel.mention}",
            color="success"
        )
        await ctx.send(embed=embed)

    @bot.command(name='setlogs')
    @has_admin_permissions()
    async def set_log_channel(ctx, channel: discord.TextChannel):
        """Set moderation log channel"""
        settings = load_guild_settings(ctx.guild.id)
        settings["log_channel"] = channel.id
        
        embed = create_embed(
            title="✅ Log Channel Set",
            description=f"Moderation logs will be sent to {channel.mention}",
            color="success"
        )
        await ctx.send(embed=embed)
        await log_action(ctx.guild, f"📝 Log channel set to {channel.mention} by {ctx.author.mention}")

    print("👑 Admin commands loaded")
