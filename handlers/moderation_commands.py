import discord
from discord.ext import commands
import asyncio
from utils.helpers import create_embed

def has_mod_permissions():
    """Check if user has moderation permissions"""
    def predicate(ctx):
        return ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def setup_moderation_commands(bot):
    """Setup moderation commands"""

    @bot.command(name='kick')
    @has_mod_permissions()
    async def kick_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member"""
        try:
            await member.kick(reason=reason)

            embed = create_embed(
                title="👢 Member Kicked",
                description=f"{member.mention} has been kicked",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = create_embed(
                title="❌ Permission Error",
                description="I don't have permission to kick this member!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='ban')
    @has_mod_permissions()
    async def ban_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member"""
        try:
            await member.ban(reason=reason)

            embed = create_embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned",
                color="error"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = create_embed(
                title="❌ Permission Error",
                description="I don't have permission to ban this member!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='mute')
    @has_mod_permissions()
    async def mute_member(ctx, member: discord.Member, duration: int = 10, *, reason="No reason provided"):
        """Timeout a member"""
        try:
            timeout_duration = discord.utils.utcnow() + discord.timedelta(minutes=duration)
            await member.timeout(timeout_duration, reason=reason)

            embed = create_embed(
                title="🔇 Member Muted",
                description=f"{member.mention} has been muted for {duration} minutes",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = create_embed(
                title="❌ Permission Error",
                description="I don't have permission to timeout this member!",
                color="error"
            )
            await ctx.send(embed=embed)

    print("🛡️ Moderation commands loaded")