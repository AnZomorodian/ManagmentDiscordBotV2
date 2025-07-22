
import discord
from discord.ext import commands
import time
from utils.helpers import create_embed

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

    @bot.command(name='userinfo', aliases=['ui', 'user'])
    async def user_info(ctx, member: discord.Member = None):
        """User information"""
        if member is None:
            member = ctx.author

        embed = create_embed(
            title=f"👤 {member.display_name}",
            description=f"User information for {member.mention}",
            color="info",
            thumbnail=member.display_avatar.url
        )

        embed.add_field(name="📝 Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="🤖 Bot", value="Yes" if member.bot else "No", inline=True)

        created_at = discord.utils.format_dt(member.created_at, style='F')
        joined_at = discord.utils.format_dt(member.joined_at, style='F')
        
        embed.add_field(name="📅 Account Created", value=created_at, inline=True)
        embed.add_field(name="📥 Joined Server", value=joined_at, inline=True)
        embed.add_field(name="📊 Status", value=str(member.status).title(), inline=True)

        if member.roles[1:]:  # Exclude @everyone role
            roles = [role.mention for role in member.roles[1:]]
            if len(roles) <= 10:
                embed.add_field(name="🎭 Roles", value=" ".join(roles), inline=False)
            else:
                embed.add_field(name="🎭 Roles", value=f"{len(roles)} roles", inline=False)

        await ctx.send(embed=embed)

    @bot.command(name='botstats', aliases=['stats', 'botinfo'])
    async def bot_stats(ctx):
        """Bot statistics and information"""
        embed = create_embed(
            title="🤖 Bot Statistics",
            description="Amazing Management Bot v3.1",
            color="info",
            thumbnail=bot.user.display_avatar.url
        )

        # Basic stats
        total_members = sum(guild.member_count for guild in bot.guilds)
        embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds):,}", inline=True)
        embed.add_field(name="👥 Total Members", value=f"{total_members:,}", inline=True)
        embed.add_field(name="📡 Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)

        # Commands
        embed.add_field(name="⚡ Commands", value=f"{len(bot.commands)}", inline=True)
        embed.add_field(name="🎭 Events", value="7 Active", inline=True)
        embed.add_field(name="🔧 Version", value="v3.1", inline=True)

        await ctx.send(embed=embed)

    @bot.command(name='help', aliases=['h', 'commands'])
    async def help_command(ctx, category=None):
        """Show help information"""
        if category is None:
            embed = create_embed(
                title="📚 Amazing Management Bot - Help",
                description="Use `!help <category>` for specific command categories",
                color="info"
            )

            embed.add_field(
                name="📊 Information Commands",
                value="`!help info` - Server & user information",
                inline=False
            )
            embed.add_field(
                name="👑 Admin Commands", 
                value="`!help admin` - Administrative tools",
                inline=False
            )
            embed.add_field(
                name="🛡️ Moderation Commands",
                value="`!help mod` - Moderation tools",
                inline=False
            )
            embed.add_field(
                name="🎪 Fun Commands",
                value="`!help fun` - Entertainment & games",
                inline=False
            )

        elif category.lower() in ['info', 'information']:
            embed = create_embed(
                title="📊 Information Commands",
                description="Server and user information commands",
                color="info"
            )
            embed.add_field(name="!serverinfo", value="Show server information", inline=False)
            embed.add_field(name="!userinfo [@user]", value="Show user information", inline=False)
            embed.add_field(name="!botstats", value="Show bot statistics", inline=False)

        elif category.lower() in ['admin', 'administrator']:
            embed = create_embed(
                title="👑 Admin Commands",
                description="Administrative commands (Admin only)",
                color="admin"
            )
            embed.add_field(name="!setup", value="Complete bot setup", inline=False)
            embed.add_field(name="!settrigger #channel", value="Set voice trigger channel", inline=False)

        elif category.lower() in ['mod', 'moderation']:
            embed = create_embed(
                title="🛡️ Moderation Commands", 
                description="Moderation tools (Manage Messages perm required)",
                color="warning"
            )
            embed.add_field(name="!clear [amount]", value="Delete messages", inline=False)
            embed.add_field(name="!kick @user [reason]", value="Kick a user", inline=False)
            embed.add_field(name="!ban @user [reason]", value="Ban a user", inline=False)

        elif category.lower() in ['fun', 'entertainment']:
            embed = create_embed(
                title="🎪 Fun Commands",
                description="Entertainment and game commands",
                color="success"
            )
            embed.add_field(name="!ping", value="Check bot latency", inline=False)
            embed.add_field(name="!roll [sides]", value="Roll a dice", inline=False)
            embed.add_field(name="!flip", value="Flip a coin", inline=False)
            embed.add_field(name="!8ball <question>", value="Ask the magic 8-ball", inline=False)

        else:
            embed = create_embed(
                title="❌ Invalid Category",
                description="Available categories: `info`, `admin`, `mod`, `fun`",
                color="error"
            )

        await ctx.send(embed=embed)

    print("📊 Info commands loaded successfully")
