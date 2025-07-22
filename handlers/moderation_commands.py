
import discord
import datetime
from discord.ext import commands
from utils.helpers import has_admin_permissions, log_action, create_embed
from utils.database import add_moderation_log

def setup_moderation_commands(bot):
    """Setup moderation commands"""
    
    @bot.command(name='purge', aliases=['clear', 'delete'])
    @has_admin_permissions()
    async def purge_messages(ctx, amount: int):
        """Delete multiple messages"""
        if amount < 1 or amount > 100:
            return await ctx.send("❌ Amount must be between 1 and 100")
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        embed = create_embed(
            title="🗑️ Messages Purged",
            description=f"Deleted {len(deleted)-1} messages from {ctx.channel.mention}",
            color="warning"
        )
        
        msg = await ctx.send(embed=embed, delete_after=5)
        await log_action(ctx.guild, f"🗑️ {ctx.author.mention} purged {len(deleted)-1} messages in {ctx.channel.mention}")
        add_moderation_log(ctx.guild.id, "PURGE", ctx.author.id, ctx.channel.id, f"{len(deleted)-1} messages")

    @bot.command(name='kick')
    @has_admin_permissions()
    async def kick_member(ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Kick a member from the server"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send("❌ You cannot kick someone with a higher or equal role!")
        
        try:
            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            
            embed = create_embed(
                title="👢 Member Kicked",
                description=f"{member.mention} has been kicked from the server",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            await log_action(ctx.guild, f"👢 {member.mention} was kicked by {ctx.author.mention}\n**Reason:** {reason}")
            add_moderation_log(ctx.guild.id, "KICK", ctx.author.id, member.id, reason)
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick this member")

    @bot.command(name='ban')
    @has_admin_permissions()
    async def ban_member(ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Ban a member from the server"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send("❌ You cannot ban someone with a higher or equal role!")
        
        try:
            await member.ban(reason=f"Banned by {ctx.author}: {reason}")
            
            embed = create_embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned from the server",
                color="error"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            await log_action(ctx.guild, f"🔨 {member.mention} was banned by {ctx.author.mention}\n**Reason:** {reason}")
            add_moderation_log(ctx.guild.id, "BAN", ctx.author.id, member.id, reason)
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this member")

    @bot.command(name='mute', aliases=['timeout'])
    @has_admin_permissions()
    async def timeout_member(ctx, member: discord.Member, duration: int = 60, *, reason: str = "No reason provided"):
        """Timeout a member (in minutes)"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send("❌ You cannot mute someone with a higher or equal role!")
        
        if duration > 10080:  # 7 days max
            duration = 10080
        
        try:
            timeout_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=f"Muted by {ctx.author}: {reason}")
            
            embed = create_embed(
                title="🔇 Member Muted",
                description=f"{member.mention} has been muted for {duration} minutes",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            await log_action(ctx.guild, f"🔇 {member.mention} was muted for {duration} minutes by {ctx.author.mention}\n**Reason:** {reason}")
            add_moderation_log(ctx.guild.id, "MUTE", ctx.author.id, member.id, f"{duration}min - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to timeout this member")

    print("🛡️ Moderation commands loaded")
