
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

    @bot.command(name='clear', aliases=['purge', 'delete'])
    @has_mod_permissions()
    async def clear_messages(ctx, amount: int = 10):
        """Clear messages from channel"""
        if amount < 1 or amount > 100:
            embed = create_embed(
                title="❌ Invalid Amount",
                description="Please provide a number between 1 and 100",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
            
            embed = create_embed(
                title="🗑️ Messages Cleared",
                description=f"Successfully deleted {len(deleted) - 1} messages!",
                color="success"
            )
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await msg.delete()
            
        except discord.Forbidden:
            embed = create_embed(
                title="❌ Missing Permissions",
                description="I don't have permission to delete messages!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member"""
        if member == ctx.author:
            embed = create_embed(
                title="❌ Cannot Kick Self",
                description="You cannot kick yourself!",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = create_embed(
                title="❌ Insufficient Permissions",
                description="You cannot kick someone with equal or higher role!",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            
            embed = create_embed(
                title="👢 Member Kicked",
                description=f"{member.mention} has been kicked",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = create_embed(
                title="❌ Missing Permissions",
                description="I don't have permission to kick members!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member"""
        if member == ctx.author:
            embed = create_embed(
                title="❌ Cannot Ban Self",
                description="You cannot ban yourself!",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = create_embed(
                title="❌ Insufficient Permissions",
                description="You cannot ban someone with equal or higher role!",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.ban(reason=f"Banned by {ctx.author}: {reason}")
            
            embed = create_embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned",
                color="error"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = create_embed(
                title="❌ Missing Permissions",
                description="I don't have permission to ban members!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban_member(ctx, user_id: int):
        """Unban a member by ID"""
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            
            embed = create_embed(
                title="✅ Member Unbanned",
                description=f"{user.mention} has been unbanned",
                color="success"
            )
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            embed = create_embed(
                title="❌ User Not Found",
                description="User not found or not banned!",
                color="error"
            )
            await ctx.send(embed=embed)

    print("🛡️ Moderation commands loaded successfully")
