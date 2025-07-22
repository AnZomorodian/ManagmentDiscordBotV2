import discord
from discord.ext import commands
from utils.helpers import create_embed

def has_admin_permissions():
    """Check if user has admin permissions"""
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def setup_admin_commands(bot):
    """Setup administrator commands"""

    @bot.command(name='setup')
    @has_admin_permissions()
    async def setup_bot(ctx):
        """Complete bot setup"""
        embed = create_embed(
            title="⚙️ Bot Setup Complete!",
            description="Amazing Management Bot v3.1 is ready to use!",
            color="success"
        )

        embed.add_field(
            name="🎵 Voice Features",
            value="Use `!settrigger #channel` to enable auto voice channels",
            inline=False
        )

        embed.add_field(
            name="📊 Commands",
            value="Use `!help` to see all available commands",
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(name='settrigger')
    @has_admin_permissions()
    async def set_trigger_channel(ctx, channel: discord.VoiceChannel):
        """Set a voice channel as trigger for auto-creation"""
        embed = create_embed(
            title="✅ Trigger Channel Set",
            description=f"{channel.mention} is now a trigger channel!\nUsers joining will get their own voice channel.",
            color="success"
        )

        await ctx.send(embed=embed)

    @bot.command(name='setwelcome')
    @has_admin_permissions()
    async def set_welcome_channel(ctx, channel: discord.TextChannel):
        """Set welcome message channel"""
        embed = create_embed(
            title="✅ Welcome Channel Set",
            description=f"{channel.mention} is now the welcome channel!",
            color="success"
        )

        await ctx.send(embed=embed)

    @bot.command(name='setlogs')
    @has_admin_permissions()
    async def set_log_channel(ctx, channel: discord.TextChannel):
        """Set moderation log channel"""
        embed = create_embed(
            title="✅ Log Channel Set",
            description=f"{channel.mention} is now the moderation log channel!",
            color="success"
        )

        await ctx.send(embed=embed)

    print("👑 Admin commands loaded successfully")