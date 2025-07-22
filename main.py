
import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIXES = ['!', '?', '.']
BOT_VERSION = "3.2"

# Enhanced intents
intents = discord.Intents.all()

# Bot initialization
bot = commands.Bot(
    command_prefix=PREFIXES,
    intents=intents,
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    description=f"Amazing Discord Management Bot v{BOT_VERSION}"
)

# Import handlers after bot initialization
from handlers.events import setup_events
from handlers.commands import setup_commands

@bot.event
async def on_ready():
    """Bot ready event with enhanced status"""
    print("=" * 60)
    print(f"🎉 {bot.user.name} is now ONLINE!")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} server(s)")
    print(f"👥 Serving {sum(guild.member_count for guild in bot.guilds)} members")
    print(f"📡 Latency: {round(bot.latency * 1000)}ms")
    print(f"🔧 Version: v{BOT_VERSION}")
    print("=" * 60)
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers | v{BOT_VERSION}"
        ),
        status=discord.Status.online
    )

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Missing Permissions",
            description="You don't have permission to use this command!",
            color=0xff0000
        )
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="❌ Bot Missing Permissions",
            description="I don't have the required permissions to execute this command!",
            color=0xff0000
        )
        await ctx.send(embed=embed, delete_after=10)
    else:
        embed = discord.Embed(
            title="❌ An Error Occurred",
            description=f"```{str(error)}```",
            color=0xff0000
        )
        await ctx.send(embed=embed, delete_after=15)
        print(f"Command error: {error}")

async def main():
    """Main bot function with comprehensive error handling"""
    try:
        print("🚀 Starting Amazing Management Bot v3.2...")
        print("🔐 Loading secure .env configuration...")

        # Validate token
        if not TOKEN:
            print("❌ DISCORD_TOKEN not found in .env file!")
            print("💡 Please add DISCORD_TOKEN=your_token_here to your .env file")
            return

        if len(TOKEN) < 50:
            print("❌ Invalid Discord token format!")
            print("💡 Please check your DISCORD_TOKEN in the .env file")
            return

        print("✅ Discord token found and validated")
        print("✅ Environment validation passed!")

        # Setup bot components
        print("⚙️ Setting up bot components...")
        
        try:
            setup_events(bot)
            setup_commands(bot)
            print("✅ All components loaded successfully")
        except Exception as e:
            print(f"❌ Error setting up components: {e}")
            return

        print("🌟 All systems ready! Starting bot...")

        # Run the bot
        await bot.start(TOKEN)

    except discord.LoginFailure:
        print("❌ Login Error: Invalid Discord token!")
        print("💡 Please check your DISCORD_TOKEN in the .env file")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
