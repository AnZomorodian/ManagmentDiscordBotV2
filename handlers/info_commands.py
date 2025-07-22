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

    @bot.command(name='mystats', aliases=['stats', 'me'])
    async def my_stats(ctx):
        """Show your personal bot statistics with achievements"""
        from utils.database import update_user_command_stats
        
        # Update command usage
        update_user_command_stats(ctx.author.id)
        
        stats = get_user_stats(ctx.author.id)

        embed = create_embed(
            title=f"📊 {ctx.author.display_name}'s Statistics",
            description="Your Amazing Management Bot v3.1 activity",
            color="info",
            thumbnail=ctx.author.display_avatar.url
        )

        embed.add_field(name="🎵 Channels Created", value=f"{stats['channels_created']:,}", inline=True)
        embed.add_field(name="⚡ Commands Used", value=f"{stats['commands_used']:,}", inline=True)
        embed.add_field(name="⌚ Voice Time", value=f"{stats['total_time']} min", inline=True)

        # Calculate rank based on channel creation
        sorted_users = sorted(user_stats.keys(), key=lambda x: user_stats[x]['channels_created'], reverse=True)
        rank = sorted_users.index(ctx.author.id) + 1 if ctx.author.id in sorted_users else len(user_stats) + 1
        embed.add_field(name="🏆 Global Rank", value=f"#{rank}", inline=True)
        
        # Activity metrics
        embed.add_field(name="📨 Voice Joins", value=f"{stats['voice_joins']:,}", inline=True)
        embed.add_field(name="💬 Messages", value=f"{stats['messages_sent']:,}", inline=True)

        # Enhanced achievements system
        achievements = []
        if stats['channels_created'] >= 1:
            achievements.append("🆕 First Channel")
        if stats['channels_created'] >= 5:
            achievements.append("🏠 Channel Builder")
        if stats['channels_created'] >= 25:
            achievements.append("🏗️ Architect")
        if stats['channels_created'] >= 100:
            achievements.append("🏛️ Master Builder")
        
        if stats['commands_used'] >= 10:
            achievements.append("🎮 Getting Started")
        if stats['commands_used'] >= 50:
            achievements.append("⚡ Active User")
        if stats['commands_used'] >= 200:
            achievements.append("🔥 Power User")
        if stats['commands_used'] >= 1000:
            achievements.append("👑 Bot Master")
            
        if stats['total_time'] >= 60:  # 1 hour
            achievements.append("🎵 Voice User")
        if stats['total_time'] >= 720:  # 12 hours
            achievements.append("🎤 Voice Enthusiast")
        if stats['total_time'] >= 1440:  # 24 hours
            achievements.append("🏆 Voice Champion")
            
        if achievements:
            embed.add_field(name="🏆 Achievements", value="\n".join(achievements), inline=False)
        else:
            embed.add_field(name="🏆 Achievements", value="Use commands to unlock achievements!", inline=False)
            
        # Add activity status
        if stats['last_active']:
            from datetime import datetime
            try:
                last_active = datetime.fromisoformat(stats['last_active'])
                embed.set_footer(text=f"Last active: {last_active.strftime('%B %d, %Y at %I:%M %p')}")
            except:
                embed.set_footer(text="Member of Amazing Management Bot community")
        else:
            embed.set_footer(text="Welcome to Amazing Management Bot!")

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
        """Enhanced help command with v3.1 features"""
        is_admin = ctx.author.guild_permissions.administrator

        embed = create_embed(
            title="🤖 Amazing Management Bot v3.1 - Command Center",
            description=f"🚀 **Enhanced Modular Architecture**\n{'👑 **ADMINISTRATOR ACCESS**' if is_admin else '👤 **STANDARD USER ACCESS**'}",
            color="admin" if is_admin else "info"
        )

        if is_admin:
            embed.add_field(
                name="👑 **ADMIN COMMANDS**",
                value=(
                    "• `!setup` - Complete bot configuration\n"
                    "• `!setwelcome #channel` - Set welcome channel\n"
                    "• `!setlogs #channel` - Set log channel\n"
                    "• `!settrigger #voice` - Voice trigger setup\n"
                    "• `!voicesettings` - Voice configuration\n"
                    "• `!autorole @role` - Auto role assignment"
                ),
                inline=False
            )

            embed.add_field(
                name="🛡️ **MODERATION**",
                value=(
                    "• `!purge <amount>` - Bulk delete messages\n"
                    "• `!kick @user [reason]` - Kick member\n"
                    "• `!ban @user [reason]` - Ban member\n"
                    "• `!mute @user <time> [reason]` - Timeout member\n"
                    "• `!warn @user [reason]` - Issue warning"
                ),
                inline=False
            )

        embed.add_field(
            name="🆕 **v3.1 NEW FEATURES**",
            value=(
                "• Enhanced achievements system\n"
                "• Improved statistics tracking\n"
                "• Better error handling\n"
                "• Fixed command conflicts\n"
                "• Enhanced security with .env\n"
                "• Performance optimizations"
            ),
            inline=False
        )

        embed.add_field(
            name="📊 **INFORMATION**",
            value=(
                "• `!serverinfo` - Detailed server statistics\n"
                "• `!mystats` - Personal achievements & stats\n"
                "• `!botstats` - Bot performance metrics\n"
                "• `!userinfo @user` - User information"
            ),
            inline=False
        )

        embed.add_field(
            name="🎪 **FUN & GAMES**",
            value=(
                "• `!ping` - Check bot responsiveness\n"
                "• `!roll 6` or `!roll 2d20+5` - Advanced dice rolling\n"
                "• `!8ball <question>` - Magic 8-ball predictions\n"
                "• `!flip` - Coin flip with style\n"
                "• `!choose option1, option2, option3` - Random picker"
            ),
            inline=False
        )

        embed.set_footer(text="Use !help <command> for detailed help on specific commands")
        await ctx.send(embed=embed)

    @bot.command(name='leaderboard', aliases=['top', 'lb'])
    async def leaderboard(ctx):
        """Show server leaderboard"""
        from utils.database import get_top_users
        
        top_users = get_top_users(10)
        
        if not top_users:
            embed = create_embed(
                title="🏆 Server Leaderboard",
                description="No activity recorded yet! Start using the bot to appear here.",
                color="info"
            )
            await ctx.send(embed=embed)
            return
        
        embed = create_embed(
            title="🏆 Server Leaderboard - Top Channel Creators",
            description="Most active community members",
            color="success"
        )
        
        leaderboard_text = ""
        for i, (user_id, stats) in enumerate(top_users, 1):
            try:
                user = bot.get_user(user_id)
                if user:
                    username = user.display_name
                else:
                    username = f"User#{user_id}"
            except:
                username = f"User#{user_id}"
                
            emoji = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            leaderboard_text += f"{emoji} **{username}** - {stats['channels_created']} channels\n"
        
        embed.add_field(name="Top Creators", value=leaderboard_text, inline=False)
        embed.set_footer(text="Use !mystats to see your detailed statistics")
        
        await ctx.send(embed=embed)

    print("📊 Info commands loaded")