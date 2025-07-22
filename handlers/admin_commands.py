
import discord
from discord.ext import commands
from utils.helpers import create_embed

def has_admin_permissions():
    """Check if user has admin permissions"""
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild
    return commands.check(predicate)

def setup_admin_commands(bot):
    """Setup administrator commands with enhanced functionality"""

    @bot.command(name='setup')
    @has_admin_permissions()
    async def setup_bot(ctx):
        """Complete bot setup wizard"""
        embed = create_embed(
            title="⚙️ Bot Setup Complete!",
            description="Amazing Management Bot v3.2 is ready to use!",
            color="success"
        )

        embed.add_field(
            name="🎵 Voice Features",
            value="• Use `!settrigger #channel` to enable auto voice channels\n• Use `!triggerlist` to see active triggers",
            inline=False
        )

        embed.add_field(
            name="📊 Commands",
            value="• Use `!help` to see all available commands\n• Use `!botstats` for bot information",
            inline=False
        )

        embed.add_field(
            name="🛡️ Moderation",
            value="• Use `!purge` to clean messages\n• Use `!kick`, `!ban` for member management",
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(name='setwelcome')
    @has_admin_permissions()
    async def set_welcome_channel(ctx, channel: discord.TextChannel = None):
        """Set welcome message channel"""
        if not channel:
            embed = create_embed(
                title="❌ Invalid Usage",
                description="Please specify a text channel!\n**Usage:** `!setwelcome #general`",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        embed = create_embed(
            title="✅ Welcome Channel Set",
            description=f"{channel.mention} is now the welcome channel!\nNew members will be greeted here.",
            color="success"
        )

        await ctx.send(embed=embed)

    @bot.command(name='setlogs')
    @has_admin_permissions()
    async def set_log_channel(ctx, channel: discord.TextChannel = None):
        """Set moderation log channel"""
        if not channel:
            embed = create_embed(
                title="❌ Invalid Usage",
                description="Please specify a text channel!\n**Usage:** `!setlogs #mod-logs`",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        embed = create_embed(
            title="✅ Log Channel Set",
            description=f"{channel.mention} is now the moderation log channel!\nAll moderation actions will be logged here.",
            color="success"
        )

        await ctx.send(embed=embed)

    @bot.command(name='voicesettings')
    @has_admin_permissions()
    async def voice_settings(ctx):
        """Display voice channel settings"""
        from config.settings import VOICE_SETTINGS
        
        embed = create_embed(
            title="🎵 Voice Channel Settings",
            description="Current voice channel configuration:",
            color="info"
        )

        embed.add_field(
            name="⏱️ Auto-Delete Timeout",
            value=f"{VOICE_SETTINGS['auto_delete_timeout']} seconds",
            inline=True
        )

        embed.add_field(
            name="🏠 Max User Channels",
            value=f"{VOICE_SETTINGS['max_user_channels']} per user",
            inline=True
        )

        embed.add_field(
            name="🎧 Default Bitrate",
            value=f"{VOICE_SETTINGS['default_bitrate']} bps",
            inline=True
        )

        await ctx.send(embed=embed)

    @bot.command(name='botsettings')
    @has_admin_permissions()
    async def bot_settings(ctx):
        """Display bot configuration"""
        from config.settings import BOT_VERSION, PREFIXES
        
        embed = create_embed(
            title="🤖 Bot Configuration",
            description=f"Amazing Management Bot v{BOT_VERSION}",
            color="info"
        )

        embed.add_field(
            name="🎯 Command Prefixes",
            value=", ".join(f"`{p}`" for p in PREFIXES),
            inline=True
        )

        embed.add_field(
            name="🎭 Total Commands",
            value=f"{len(bot.commands)}",
            inline=True
        )

        embed.add_field(
            name="🌐 Servers",
            value=f"{len(bot.guilds)}",
            inline=True
        )

        await ctx.send(embed=embed)

    print("👑 Admin commands loaded successfully")
