
import discord
import datetime
from discord.ext import commands
from utils.helpers import has_admin_permissions, log_action, create_embed
from utils.database import add_moderation_log

def setup_moderation_commands(bot):
    """Setup moderation commands"""
    
    @bot.command(name='purge', aliases=['clear', 'clean'])
    @has_admin_permissions()
    async def purge_messages(ctx, amount: int = 10):
        """Purge messages from channel"""
        if amount > 100:
            amount = 100
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            embed = create_embed(
                title="🧹 Messages Purged",
                description=f"Successfully deleted {len(deleted)-1} messages",
                color="success"
            )
            
            # Add to moderation logs
            add_moderation_log(
                ctx.guild.id, 
                "PURGE", 
                ctx.author.id, 
                ctx.channel.id, 
                f"Purged {len(deleted)-1} messages"
            )
            
            await ctx.send(embed=embed, delete_after=5)
            
        except Exception as e:
            embed = create_embed(
                title="❌ Purge Failed",
                description=f"Error: {str(e)[:100]}",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='kick')
    @has_admin_permissions()
    async def kick_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server"""
        try:
            await member.kick(reason=reason)
            
            embed = create_embed(
                title="👢 Member Kicked",
                description=f"**{member.mention}** has been kicked",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            # Add to moderation logs
            add_moderation_log(ctx.guild.id, "KICK", ctx.author.id, member.id, reason)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = create_embed(
                title="❌ Kick Failed",
                description=f"Error: {str(e)[:100]}",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='ban')
    @has_admin_permissions()
    async def ban_member(ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server"""
        try:
            await member.ban(reason=reason)
            
            embed = create_embed(
                title="🔨 Member Banned",
                description=f"**{member.mention}** has been banned",
                color="error"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            # Add to moderation logs
            add_moderation_log(ctx.guild.id, "BAN", ctx.author.id, member.id, reason)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = create_embed(
                title="❌ Ban Failed",
                description=f"Error: {str(e)[:100]}",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='mute', aliases=['timeout'])
    @has_admin_permissions()
    async def mute_member(ctx, member: discord.Member, duration: int = 60, *, reason="No reason provided"):
        """Timeout a member"""
        try:
            timeout_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=reason)
            
            embed = create_embed(
                title="🔇 Member Muted",
                description=f"**{member.mention}** has been muted for {duration} minutes",
                color="warning"
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            
            # Add to moderation logs
            add_moderation_log(ctx.guild.id, "MUTE", ctx.author.id, member.id, f"{reason} ({duration}m)")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = create_embed(
                title="❌ Mute Failed",
                description=f"Error: {str(e)[:100]}",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='modlogs', aliases=['logs'])
    @has_admin_permissions()
    async def moderation_logs(ctx, limit: int = 10):
        """Show recent moderation logs"""
        from utils.database import get_moderation_logs
        
        logs = get_moderation_logs(ctx.guild.id, limit)
        
        if not logs:
            embed = create_embed(
                title="📋 Moderation Logs",
                description="No moderation actions recorded yet.",
                color="info"
            )
            await ctx.send(embed=embed)
            return
        
        embed = create_embed(
            title="📋 Recent Moderation Logs",
            description=f"Showing last {len(logs)} actions",
            color="moderation"
        )
        
        for log in logs[-5:]:  # Show last 5 logs
            moderator = bot.get_user(log['moderator'])
            target = bot.get_user(log['target']) if isinstance(log['target'], int) else f"Channel #{log['target']}"
            
            embed.add_field(
                name=f"{log['action']} - {log['timestamp'].strftime('%H:%M %d/%m')}",
                value=f"**Mod:** {moderator.mention if moderator else 'Unknown'}\n**Target:** {target}\n**Reason:** {log['reason'][:50]}",
                inline=True
            )
        
        await ctx.send(embed=embed)
