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
        """Set welcome channel"""
        embed = create_embed(
            title="✅ Welcome Channel Set",
            description=f"Welcome messages will be sent to {channel.mention}",
            color="success"
        )
        await ctx.send(embed=embed)

    @bot.command(name='setlogs')
    @has_admin_permissions()
    async def set_log_channel(ctx, channel: discord.TextChannel):
        """Set log channel"""
        embed = create_embed(
            title="✅ Log Channel Set",
            description=f"Moderation logs will be sent to {channel.mention}",
            color="success"
        )
        await ctx.send(embed=embed)

    @bot.command(name='purge')
    @has_admin_permissions()
    async def purge_messages(ctx, amount: int):
        """Delete messages"""
        if amount > 100:
            amount = 100

        deleted = await ctx.channel.purge(limit=amount + 1)

        embed = create_embed(
            title="🗑️ Messages Deleted",
            description=f"Deleted {len(deleted) - 1} messages",
            color="success"
        )

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

    print("👑 Admin commands loaded")