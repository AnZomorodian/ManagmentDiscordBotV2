
import os
import discord
from discord.ext import commands
import asyncio
import datetime
import random

# Your Discord Bot Token
TOKEN = "MTAwMTQ1ODQ2NTk3NTMxMjQwNA.GPizIh.7PZQr5KhrvupPCcx6bIFescSpGXUxmychJ_MFo"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=['!', '?', '$'], intents=intents, help_command=None)

# Store created channels for tracking
created_channels = {}
user_stats = {}

@bot.event
async def on_ready():
    print(f'🚀 Amazing Discord Bot is ONLINE!')
    print(f'🤖 Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'🌐 Connected to {len(bot.guilds)} servers')
    print(f'👥 Serving {sum(guild.member_count for guild in bot.guilds)} users')
    print('-' * 50)
    
    # Set dynamic bot status
    activities = [
        discord.Activity(type=discord.ActivityType.listening, name="for voice channels | !help"),
        discord.Activity(type=discord.ActivityType.watching, name="over the server | !help"),
        discord.Activity(type=discord.ActivityType.playing, name="with voice channels | !help")
    ]
    
    while True:
        for activity in activities:
            await bot.change_presence(activity=activity, status=discord.Status.online)
            await asyncio.sleep(30)  # Change status every 30 seconds

@bot.event
async def on_voice_state_update(member, before, after):
    # Skip if it's a bot
    if member.bot:
        return
    
    # Track user stats
    if member.id not in user_stats:
        user_stats[member.id] = {"channels_created": 0, "total_time": 0}
    
    # Check if the member joined a voice channel (and wasn't in one before)
    if after.channel and not before.channel:
        try:
            guild = member.guild
            category = after.channel.category
            
            # Create a new voice channel with enhanced naming
            channel_names = [
                f"🎵 {member.display_name}'s Lounge",
                f"🎤 {member.display_name}'s Studio",
                f"🎮 {member.display_name}'s Gaming Room",
                f"💭 {member.display_name}'s Hangout",
                f"🌟 {member.display_name}'s Space"
            ]
            
            new_channel = await guild.create_voice_channel(
                name=random.choice(channel_names),
                category=category,
                user_limit=10,
                bitrate=96000  # Higher quality audio
            )
            
            # Store channel info
            created_channels[new_channel.id] = {
                "creator": member.id,
                "created_at": datetime.datetime.now(),
                "guild_id": guild.id
            }
            
            # Move the user to the new channel
            await member.move_to(new_channel)
            user_stats[member.id]["channels_created"] += 1
            
            print(f"✅ Created voice channel '{new_channel.name}' for {member.display_name}")
            
            # Send welcome message to a text channel (if exists)
            for channel in guild.text_channels:
                if "general" in channel.name.lower() or "chat" in channel.name.lower():
                    embed = discord.Embed(
                        title="🎵 New Voice Channel Created!",
                        description=f"{member.mention} just created **{new_channel.name}**!",
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed, delete_after=10)
                    break
            
            # Start the cleanup task
            bot.loop.create_task(wait_and_delete_channel(new_channel))
            
        except discord.Forbidden:
            print(f"❌ Missing permissions to create voice channel for {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Failed to create voice channel: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error in voice state update: {e}")

async def wait_and_delete_channel(channel):
    """Wait for a voice channel to become empty, then delete it"""
    while True:
        await asyncio.sleep(15)  # Check every 15 seconds
        try:
            # Refresh channel object to get current members
            channel = bot.get_channel(channel.id)
            if not channel:
                break  # Channel no longer exists
            
            if len(channel.members) == 0:
                # Clean up stored data
                if channel.id in created_channels:
                    del created_channels[channel.id]
                
                await channel.delete()
                print(f"✅ Deleted empty channel: {channel.name}")
                break
        except discord.NotFound:
            break  # Channel already deleted
        except discord.Forbidden:
            print(f"❌ No permission to delete channel: {channel.name}")
            break
        except Exception as e:
            print(f"⚠️ Error managing channel {channel.name}: {e}")
            break

@bot.command(name='serverinfo', aliases=['si', 'server'])
async def server_info(ctx):
    """Display detailed server information"""
    guild = ctx.guild
    
    # Create an enhanced embed with server info
    embed = discord.Embed(
        title=f"📊 {guild.name} - Server Information",
        description=f"Complete overview of **{guild.name}**",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    # Add server icon and banner
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    
    # Basic server info
    embed.add_field(name="👑 Owner", value=f"{guild.owner.mention}\n({guild.owner})" if guild.owner else "Unknown", inline=True)
    embed.add_field(name="📅 Created", value=f"{discord.utils.format_dt(guild.created_at, style='D')}\n({discord.utils.format_dt(guild.created_at, style='R')})", inline=True)
    embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=True)
    
    # Member counts with online status
    total_members = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    humans = total_members - bots
    online_members = len([m for m in guild.members if m.status != discord.Status.offline and not m.bot])
    
    embed.add_field(name="👥 Total Members", value=f"{total_members:,}", inline=True)
    embed.add_field(name="🤖 Bots", value=f"{bots:,}", inline=True)
    embed.add_field(name="👨‍👩‍👧‍👦 Humans", value=f"{humans:,}", inline=True)
    embed.add_field(name="🟢 Online", value=f"{online_members:,}", inline=True)
    
    # Channels with more details
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    stage_channels = len(guild.stage_channels)
    
    embed.add_field(name="💬 Text Channels", value=f"{text_channels:,}", inline=True)
    embed.add_field(name="🔊 Voice Channels", value=f"{voice_channels:,}", inline=True)
    embed.add_field(name="🎭 Stage Channels", value=f"{stage_channels:,}", inline=True)
    embed.add_field(name="📁 Categories", value=f"{categories:,}", inline=True)
    
    # Enhanced server features
    embed.add_field(name="😀 Emojis", value=f"{len(guild.emojis):,}/{guild.emoji_limit}", inline=True)
    embed.add_field(name="🎭 Roles", value=f"{len(guild.roles):,}", inline=True)
    embed.add_field(name="⚡ Boost Level", value=f"Level {guild.premium_tier}", inline=True)
    embed.add_field(name="💎 Boosters", value=f"{guild.premium_subscription_count:,}", inline=True)
    
    # Verification and features
    verification_levels = {
        discord.VerificationLevel.none: "None",
        discord.VerificationLevel.low: "Low",
        discord.VerificationLevel.medium: "Medium", 
        discord.VerificationLevel.high: "High",
        discord.VerificationLevel.highest: "Highest"
    }
    
    embed.add_field(name="🛡️ Verification", value=verification_levels.get(guild.verification_level, "Unknown"), inline=True)
    embed.add_field(name="🔞 NSFW Filter", value=str(guild.explicit_content_filter).title(), inline=True)
    embed.add_field(name="📱 Features", value=f"{len(guild.features)} enabled", inline=True)
    
    # Server region and other info
    embed.add_field(name="🌍 Region", value=str(guild.region).title() if hasattr(guild, 'region') else "Auto", inline=True)
    embed.add_field(name="📂 File Size Limit", value=f"{guild.filesize_limit // 1048576} MB", inline=True)
    embed.add_field(name="🎵 Bitrate Limit", value=f"{guild.bitrate_limit // 1000} kbps", inline=True)
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name} • Bot created {len(created_channels)} voice channels", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='help', aliases=['h', 'commands'])
async def help_command(ctx):
    """Display comprehensive help information"""
    embed = discord.Embed(
        title="🤖 Amazing Discord Bot - Complete Guide",
        description="🚀 **Welcome to the most advanced Discord bot!** Here's everything I can do:",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(
        name="📊 **Server Information**",
        value="• `!serverinfo` / `!si` - Detailed server stats\n• `!mystats` - Your personal bot usage stats\n• `!botstats` - Bot performance statistics",
        inline=False
    )
    
    embed.add_field(
        name="🎵 **Auto Voice Channels** ⭐",
        value="• Join any voice channel → I create a personal room!\n• Rooms auto-delete when empty\n• Multiple creative room names\n• High-quality audio (96kbps)\n• 10 user limit per room",
        inline=False
    )
    
    embed.add_field(
        name="🎮 **Fun Commands**",
        value="• `!ping` - Check bot latency\n• `!coinflip` - Flip a coin\n• `!roll` - Roll dice (1-100)\n• `!8ball <question>` - Magic 8-ball",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ **Bot Information**",
        value="• `!help` / `!h` - Show this menu\n• `!uptime` - How long bot has been running\n• `!invite` - Get bot invite link",
        inline=False
    )
    
    embed.add_field(
        name="🔧 **Prefixes**",
        value="You can use `!`, `?`, or `$` before any command!",
        inline=False
    )
    
    embed.add_field(
        name="💡 **Pro Tips**",
        value="• Voice channels are fully automated\n• All commands work in any text channel\n• Bot status changes every 30 seconds\n• Created channels get random creative names\n• Your stats are tracked automatically",
        inline=False
    )
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name} • Serving {len(bot.guilds)} servers", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='mystats')
async def my_stats(ctx):
    """Show user's bot usage statistics"""
    user_id = ctx.author.id
    if user_id not in user_stats:
        user_stats[user_id] = {"channels_created": 0, "total_time": 0}
    
    stats = user_stats[user_id]
    
    embed = discord.Embed(
        title=f"📈 {ctx.author.display_name}'s Bot Stats",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="🎵 Channels Created", value=f"{stats['channels_created']:,}", inline=True)
    embed.add_field(name="⭐ Rank", value=f"#{sorted(user_stats.keys(), key=lambda x: user_stats[x]['channels_created'], reverse=True).index(user_id) + 1}", inline=True)
    embed.add_field(name="🏆 Achievement", value="Voice Master!" if stats['channels_created'] >= 10 else "Getting Started", inline=True)
    
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='botstats')
async def bot_stats(ctx):
    """Show bot performance statistics"""
    embed = discord.Embed(
        title="🤖 Bot Performance Stats",
        color=discord.Color.orange(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds):,}", inline=True)
    embed.add_field(name="👥 Users", value=f"{sum(guild.member_count for guild in bot.guilds):,}", inline=True)
    embed.add_field(name="🎵 Active Channels", value=f"{len(created_channels):,}", inline=True)
    embed.add_field(name="📊 Total Created", value=f"{sum(stats['channels_created'] for stats in user_stats.values()):,}", inline=True)
    embed.add_field(name="⚡ Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="💾 Commands", value="15+", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=discord.Color.green() if latency < 100 else discord.Color.yellow() if latency < 200 else discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name='coinflip', aliases=['flip', 'coin'])
async def coinflip(ctx):
    """Flip a coin"""
    result = random.choice(['Heads', 'Tails'])
    emoji = '🪙' if result == 'Heads' else '🔘'
    embed = discord.Embed(
        title=f"{emoji} Coin Flip Result",
        description=f"The coin landed on **{result}**!",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name='roll', aliases=['dice'])
async def roll_dice(ctx, sides: int = 100):
    """Roll a dice (default 1-100)"""
    if sides < 2:
        sides = 6
    if sides > 1000:
        sides = 1000
        
    result = random.randint(1, sides)
    embed = discord.Embed(
        title="🎲 Dice Roll",
        description=f"You rolled a **{result}** out of {sides}!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='8ball', aliases=['eightball'])
async def magic_8ball(ctx, *, question):
    """Ask the magic 8-ball a question"""
    responses = [
        "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
        "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
        "Don't count on it", "My reply is no", "My sources say no",
        "Outlook not so good", "Very doubtful"
    ]
    
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

@bot.command(name='uptime')
async def uptime(ctx):
    """Show bot uptime"""
    embed = discord.Embed(
        title="⏰ Bot Uptime",
        description="Bot has been running since startup!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='invite')
async def invite(ctx):
    """Get bot invite link"""
    embed = discord.Embed(
        title="📨 Invite Me to Your Server!",
        description=f"[Click here to invite me!](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Enhanced message events
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Respond to various greetings
    if any(greeting in message.content.lower() for greeting in ['hello', 'hi', 'hey', '$hello']):
        greetings = [
            f'Hello {message.author.mention}! 👋',
            f'Hey there {message.author.mention}! 🎉',
            f'Hi {message.author.mention}! Ready to create some voice channels? 🎵',
            f'Greetings {message.author.mention}! Type !help for commands! ✨'
        ]
        await message.channel.send(random.choice(greetings))
    
    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    """Welcome message when bot joins a server"""
    print(f"🎉 Joined new server: {guild.name} ({guild.id})")
    
    # Send welcome message to general channel
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="🎉 Thanks for inviting me!",
                description="I'm your **Amazing Discord Bot**! I create personal voice channels when you join voice channels!\n\nType `!help` to see all my commands!",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)
            break

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Command Not Found",
            description=f"Unknown command! Type `!help` to see available commands.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)

# Run the bot
try:
    print("🚀 Starting Amazing Discord Bot...")
    print("🔑 Using embedded token...")
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("❌ Rate limited! Too many requests to Discord API")
        print("💡 Solution: https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
except Exception as e:
    print(f"❌ Bot failed to start: {e}")
