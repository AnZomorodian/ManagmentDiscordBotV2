
import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from config.settings import TOKEN, PREFIXES, INTENTS, FEATURES, BOT_ACTIVITIES, BOT_VERSION
from handlers.events import setup_events
from handlers.commands import setup_commands
from utils.database import initialize_data
from utils.helpers import setup_bot_status, validate_environment

# Load environment variables first
load_dotenv()

# Enhanced bot initialization
bot = commands.Bot(
    command_prefix=PREFIXES, 
    intents=INTENTS, 
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    description=f"Amazing Discord Management Bot v{BOT_VERSION}"
)

# Initialize data storage
initialize_data()

async def on_ready_setup():
    """Setup tasks when bot is ready"""
    print("=" * 60)
    print(f"🎉 {bot.user.name} is now ONLINE and ready!")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} server(s)")
    print(f"👥 Serving {sum(guild.member_count for guild in bot.guilds)} members")
    print(f"📡 Latency: {round(bot.latency * 1000)}ms")
    print("=" * 60)

@bot.event
async def on_ready():
    """Enhanced on_ready event"""
    await on_ready_setup()

def main():
    """Enhanced main bot startup function with complete error handling"""
    try:
        print("🚀 Starting Amazing Management Bot v3.1...")
        print("🔐 Loading secure .env configuration...")
        
        # Validate environment
        if not validate_environment():
            print("❌ Environment validation failed!")
            return
            
        print("✅ Environment validation passed!")
        print(f"🔑 Discord token loaded securely from .env file")
        print(f"👑 Admin features: {'✅ Enabled' if FEATURES['moderation'] else '❌ Disabled'}")
        print(f"🎵 Voice system: {'✅ Active' if FEATURES['auto_voice'] else '❌ Disabled'}")
        print(f"🎪 Fun commands: {'✅ Loaded' if FEATURES['fun_commands'] else '❌ Disabled'}")
        print(f"📊 Statistics: {'✅ Tracking' if FEATURES['statistics'] else '❌ Disabled'}")
        print(f"🔒 Enhanced security: {'✅ Enabled' if FEATURES['enhanced_security'] else '❌ Disabled'}")
        print("📁 Modular architecture v3.1 loaded...")
        print(f"⚙️  Features: {sum(FEATURES.values())}/{len(FEATURES)} enabled")

        # Setup event handlers
        setup_events(bot)
        print("✅ Event handlers registered")

        # Setup command handlers
        setup_commands(bot)
        print("✅ Command handlers registered")

        # Setup status rotation
        asyncio.create_task(setup_bot_status(bot))
        print("✅ Status rotation configured")

        print("🌟 All systems ready! Starting bot connection...")
        print("📡 Connecting to Discord Gateway...")

        # Run the bot
        bot.run(TOKEN)

    except discord.LoginFailure:
        print("❌ Login Error: Invalid Discord token!")
        print("💡 Please check your DISCORD_TOKEN in the .env file")
        print("🔗 Get your token from: https://discord.com/developers/applications")
    except discord.HTTPException as e:
        if e.status == 429:
            print("❌ Rate limited! Too many requests to Discord API")
            print("💡 Wait a few minutes and try again")
        else:
            print(f"❌ HTTP Error: {e}")
    except discord.ConnectionClosed:
        print("❌ Connection closed by Discord")
        print("💡 This usually indicates a network issue or invalid token")
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
        print("💡 Check your .env file and bot permissions")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
