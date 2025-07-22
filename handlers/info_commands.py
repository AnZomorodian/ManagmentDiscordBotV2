import discord
import datetime
from discord.ext import commands
from utils.helpers import create_embed
from utils.database import get_user_stats, created_channels, user_activity

def setup_info_commands(bot):
    """Setup information commands"""

    @bot.command(name='serverinfo', aliases=['si', 'server'])
    async def server_info(ctx):
        """Server information"""
        guild = ctx.guild
        is_admin = ctx.author.guild_permissions.administrator

        embed = create_embed(
            title=f"📊 {guild.name} - Server Info",
            description=f"🔍 **Server overview**",
            color="admin" if is_admin else "info",
            thumbnail=guild.icon.url if guild.icon else None
        )

        total_members = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = total_members - bots
        online_members = len([m for m in guild.members if m.status != discord.Status.offline and not m.bot])

        embed.add_field(name="👥 Total Members", value=f"{total_members:,}", inline=True)
        embed.add_field(name="🤖 Bots", value=f"{bots:,}", inline=True) 
        embed.add_field(name="🟢 Online", value=f"{online_members:,}", inline=True)

        embed.add_field(name="💬 Text Channels", value=f"{len(guild.text_channels):,}", inline=True)
        embed.add_field(name="🔊 Voice Channels", value=f"{len(guild.voice_channels):,}", inline=True)
        embed.add_field(name="⚡ Boost Level", value=f"Level {guild.premium_tier}", inline=True)

        await ctx.send(embed=embed)

    @bot.command(name='mystats', aliases=['stats', 'me'])
    async def my_stats(ctx):
        """Show your personal bot statistics"""
        from utils.database import update_user_command_stats

        update_user_command_stats(ctx.author.id)
        stats = get_user_stats(ctx.author.id)

        embed = create_embed(
            title=f"📊 {ctx.author.display_name}'s Statistics",
            description="Your Amazing Management Bot activity",
            color="info",
            thumbnail=ctx.author.display_avatar.url
        )

        embed.add_field(name="🎵 Channels Created", value=f"{stats['channels_created']:,}", inline=True)
        embed.add_field(name="⚡ Commands Used", value=f"{stats['commands_used']:,}", inline=True)
        embed.add_field(name="📨 Voice Joins", value=f"{stats['voice_joins']:,}", inline=True)

        await ctx.send(embed=embed)

    @bot.command(name='botstats')
    async def bot_stats(ctx):
        """Bot performance statistics"""
        embed = create_embed(
            title="🤖 Management Bot - Stats",
            description="Bot performance metrics",
            color="info"
        )

        embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds):,}", inline=True)
        embed.add_field(name="👥 Total Users", value=f"{sum(guild.member_count for guild in bot.guilds):,}", inline=True)
        embed.add_field(name="⚡ Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)

        embed.add_field(name="🎵 Active Channels", value=f"{len(created_channels):,}", inline=True)
        embed.add_field(name="🚀 Version", value="v3.1", inline=True)

        await ctx.send(embed=embed)

    @bot.command(name='help', aliases=['h', 'commands'])
    async def help_command(ctx):
        """Help command"""
        is_admin = ctx.author.guild_permissions.administrator

        embed = create_embed(
            title="🤖 Amazing Management Bot v3.1 - Commands",
            description=f"🚀 **Bot Commands**\n{'👑 **ADMINISTRATOR ACCESS**' if is_admin else '👤 **USER ACCESS**'}",
            color="admin" if is_admin else "info"
        )

        if is_admin:
            embed.add_field(
                name="👑 **ADMIN COMMANDS**",
                value=(
                    "• `!setup` - Bot configuration\n"
                    "• `!setwelcome #channel` - Welcome channel\n"
                    "• `!setlogs #channel` - Log channel\n"
                    "• `!settrigger #voice` - Voice trigger\n"
                    "• `!purge <amount>` - Delete messages"
                ),
                inline=False
            )

        embed.add_field(
            name="📊 **INFORMATION**",
            value=(
                "• `!serverinfo` - Server statistics\n"
                "• `!mystats` - Your statistics\n"
                "• `!botstats` - Bot performance\n"
                "• `!userinfo @user` - User info"
            ),
            inline=False
        )

        embed.add_field(
            name="🎪 **FUN COMMANDS**",
            value=(
                "• `!ping` - Check responsiveness\n"
                "• `!roll 6` - Roll dice\n"
                "• `!8ball <question>` - Magic 8-ball\n"
                "• `!flip` - Coin flip"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    print("📊 Info commands loaded")