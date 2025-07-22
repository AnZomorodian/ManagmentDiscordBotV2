
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} servers')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the member joined a voice channel
    if after.channel and not before.channel:
        # Create a new voice channel for the user
        guild = member.guild
        category = after.channel.category
        
        # Create a new voice channel with the user's name
        new_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Channel",
            category=category,
            user_limit=10
        )
        
        # Move the user to the new channel
        await member.move_to(new_channel)
        
        # Delete the channel when it becomes empty
        def check_empty():
            return len(new_channel.members) == 0
        
        # Wait for the channel to become empty, then delete it
        bot.loop.create_task(wait_and_delete_channel(new_channel))

async def wait_and_delete_channel(channel):
    """Wait for a voice channel to become empty, then delete it"""
    while True:
        await discord.utils.sleep_until(discord.utils.utcnow().replace(second=0, microsecond=0) + discord.timedelta(seconds=30))
        if len(channel.members) == 0:
            try:
                await channel.delete()
                print(f"Deleted empty channel: {channel.name}")
                break
            except discord.NotFound:
                break  # Channel already deleted
            except discord.Forbidden:
                print(f"No permission to delete channel: {channel.name}")
                break

@bot.command(name='serverinfo')
async def server_info(ctx):
    """Display server information"""
    guild = ctx.guild
    
    # Create an embed with server info
    embed = discord.Embed(
        title=f"📊 {guild.name} Server Info",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    # Add server icon if available
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    # Basic server info
    embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="📅 Created", value=discord.utils.format_dt(guild.created_at, style='D'), inline=True)
    embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
    
    # Member counts
    embed.add_field(name="👥 Total Members", value=guild.member_count, inline=True)
    embed.add_field(name="🤖 Bots", value=len([m for m in guild.members if m.bot]), inline=True)
    embed.add_field(name="👨‍👩‍👧‍👦 Humans", value=len([m for m in guild.members if not m.bot]), inline=True)
    
    # Channels
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    
    embed.add_field(name="💬 Text Channels", value=text_channels, inline=True)
    embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="📁 Categories", value=categories, inline=True)
    
    # Other info
    embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="⚡ Boost Level", value=guild.premium_tier, inline=True)
    
    # Verification level
    verification_levels = {
        discord.VerificationLevel.none: "None",
        discord.VerificationLevel.low: "Low",
        discord.VerificationLevel.medium: "Medium",
        discord.VerificationLevel.high: "High",
        discord.VerificationLevel.highest: "Highest"
    }
    embed.add_field(name="🛡️ Verification Level", value=verification_levels.get(guild.verification_level, "Unknown"), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="🤖 Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="!serverinfo",
        value="Get detailed information about this server",
        inline=False
    )
    
    embed.add_field(
        name="🎵 Voice Channel Feature",
        value="Join any voice channel and I'll create a personal channel for you!",
        inline=False
    )
    
    embed.add_field(
        name="!help",
        value="Show this help message",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Keep the original $hello command for compatibility
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! 👋 Try `!help` to see what I can do!')
    
    # Process commands
    await bot.process_commands(message)

try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
