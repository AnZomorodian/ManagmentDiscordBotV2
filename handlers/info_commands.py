import discord
import datetime
from discord.ext import commands
from utils.helpers import has_admin_permissions, create_embed
from utils.database import get_user_stats, created_channels, user_stats, get_moderation_logs

def setup_info_commands(bot):
    """Setup information commands"""

    @bot.command(name='serverinfo', aliases=['si', 'server'])
    async def enhanced_server_info(ctx):
        """Enhanced server information"""
        guild = ctx.guild
        is_admin = ctx.author.guild_permissions.administrator

        embed = create_embed(
            title=f"📊 {guild.name} - Server Analysis v3.0",
            description=f"🔍 **Enhanced server overview with modular architecture**",
            color="admin" if is_admin else "info",
            thumbnail=guild.icon.url if guild.icon else None
        )

        # Enhanced statistics
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

        if is_admin:
            embed.add_field(
                name="🆕 v3.0 Features",
                value=(
                    "• Modular architecture\n"
                    "• Fixed bitrate compatibility\n"
                    "• Enhanced error handling\n"
                    "• Better performance"
                ),
                inline=False
            )

        await ctx.send(embed=embed)

    @bot.command(name='mystats')
    async def my_stats(ctx):
        """Show user's bot usage statistics"""
        stats = get_user_stats(ctx.author.id)

        embed = create_embed(
            title=f"📈 {ctx.author.display_name}'s Statistics",
            description="Your bot usage overview",
            color="info",
            thumbnail=ctx.author.display_avatar.url
        )

        embed.add_field(name="🎵 Channels Created", value=f"{stats['channels_created']:,}", inline=True)
        embed.add_field(name="📊 Commands Used", value=f"{stats['commands_used']:,}", inline=True)

        # Calculate rank
        sorted_users = sorted(user_stats.keys(), key=lambda x: user_stats[x]['channels_created'], reverse=True)
        rank = sorted_users.index(ctx.author.id) + 1 if ctx.author.id in sorted_users else "N/A"
        embed.add_field(name="🏆 Rank", value=f"#{rank}", inline=True)

        await ctx.send(embed=embed)

    @bot.command(name='botstats')
    async def bot_stats(ctx):
        """Enhanced bot performance statistics"""
        embed = create_embed(
            title="🤖 Management Bot v3.0 - Performance Dashboard",
            description="Modular architecture performance metrics",
            color="info"
        )

        embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds):,}", inline=True)
        embed.add_field(name="👥 Total Users", value=f"{sum(guild.member_count for guild in bot.guilds):,}", inline=True)
        embed.add_field(name="⚡ Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)

        embed.add_field(name="🎵 Active Channels", value=f"{len(created_channels):,}", inline=True)
        embed.add_field(name="📊 Total Created", value=f"{sum(stats['channels_created'] for stats in user_stats.values()):,}", inline=True)
        embed.add_field(name="🚀 Version", value="v3.0 Modular", inline=True)

        embed.add_field(
            name="🆕 Architecture Improvements",
            value=(
                "• Separated into multiple files\n"
                "• Better error handling\n"
                "• Fixed Discord API issues\n"
                "• Enhanced performance\n"
                "• Cleaner code structure"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(name='help', aliases=['h', 'commands'])
    async def enhanced_help(ctx):
        """Enhanced help command with v3.0 features"""
        is_admin = ctx.author.guild_permissions.administrator

        embed = create_embed(
            title="🤖 Amazing Management Bot v3.0 - Command Center",
            description=f"🚀 **Modular Architecture Edition**\n{'👑 **ADMINISTRATOR ACCESS**' if is_admin else '👤 **STANDARD USER ACCESS**'}",
            color="admin" if is_admin else "info"
        )

        if is_admin:
            embed.add_field(
                name="👑 **ADMIN COMMANDS**",
                value=(
                    "• `!setup` - Bot configuration\n"
                    "• `!setwelcome #channel` - Welcome channel\n"
                    "• `!setlogs #channel` - Log channel\n"
                    "• `!settrigger #voice` - Voice triggers\n"
                    "• `!voicesettings` - Voice config"
                ),
                inline=False
            )

            embed.add_field(
                name="🛡️ **MODERATION**",
                value=(
                    "• `!purge <amount>` - Delete messages\n"
                    "• `!kick @user` - Kick member\n"
                    "• `!ban @user` - Ban member\n"
                    "• `!mute @user` - Timeout member"
                ),
                inline=False
            )

        embed.add_field(
            name="🆕 **v3.0 IMPROVEMENTS**",
            value=(
                "• Fixed voice channel bitrate bug\n"
                "• Modular file structure\n"
                "• Enhanced error handling\n"
                "• Better performance\n"
                "• Cleaner code organization"
            ),
            inline=False
        )

        embed.add_field(
            name="📊 **INFORMATION**",
            value=(
                "• `!serverinfo` - Server stats\n"
                "• `!mystats` - Your statistics\n"
                "• `!botstats` - Bot performance"
            ),
            inline=False
        )

        embed.add_field(
            name="🎪 **FUN COMMANDS**",
            value=(
                "• `!ping` - Bot responsiveness\n"
                "• `!roll 6` or `!roll 2d20` - Roll dice\n"
                "• `!8ball <question>` - Magic 8-ball\n"
                "• `!flip` - Flip a coin\n"
                "• `!choose option1, option2` - Pick choice"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    print("📊 Info commands loaded")