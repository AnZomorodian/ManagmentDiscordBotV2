
import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from config.settings import TOKEN, PREFIXES, INTENTS, FEATURES, BOT_ACTIVITIES
from handlers.events import setup_events
from handlers.commands import setup_commands
from utils.database import initialize_data
from utils.helpers import setup_bot_status

# Load environment variables
load_dotenv()

# Initialize bot with enhanced configuration
bot = commands.Bot(
    command_prefix=PREFIXES, 
    intents=INTENTS, 
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True
)

# Initialize data storage
initialize_data()

def validate_environment():
    """Validate required environment variables"""
    if not TOKEN:
        print("❌ Critical Error: DISCORD_TOKEN not found in .env file!")
        print("💡 Please create a .env file with your Discord bot token:")
        print("   DISCORD_TOKEN=your_bot_token_here")
        return False
    return True

def main():
    """Enhanced main bot startup function"""
    try:
        print("🚀 Starting Amazing Management Bot v3.1...")
        print("🔐 Loading secure .env configuration...")
        
        # Validate environment
        if not validate_environment():
            return
            
        print("✅ Environment validation passed!")
        print("🔑 Discord token loaded securely from .env file")
        print("👑 Admin features enabled..." if FEATURES["moderation"] else "👤 Basic features only...")
        print("🎵 Smart voice trigger system ready..." if FEATURES["auto_voice"] else "🔇 Voice features disabled...")
        print("🎪 Fun commands loaded..." if FEATURES["fun_commands"] else "😐 Fun commands disabled...")
        print("📊 Statistics tracking active..." if FEATURES["statistics"] else "📊 Statistics disabled...")
        print("🔒 Enhanced security enabled..." if FEATURES["enhanced_security"] else "🔓 Basic security mode...")
        print("📁 Modular architecture v3.1 loaded...")
        print(f"⚙️  Features: {sum(FEATURES.values())}/{len(FEATURES)} enabled")

        # Setup event handlers
        setup_events(bot)

        # Setup command handlers
        setup_commands(bot)

        # Setup status rotation
        setup_bot_status(bot)

        print("🌟 All systems ready! Starting bot connection...")
        print("📡 Connecting to Discord Gateway...")

        # Run the bot
        bot.run(TOKEN)

    except discord.LoginFailure:
        print("❌ Login Error: Invalid Discord token!")
        print("💡 Please check your DISCORD_TOKEN in the .env file")
    except discord.HTTPException as e:
        if e.status == 429:
            print("❌ Rate limited! Too many requests to Discord API")
            print("💡 Wait a few minutes and try again")
        else:
            print(f"❌ HTTP Error: {e}")
    except discord.ConnectionClosed:
        print("❌ Connection closed by Discord")
        print("💡 This usually indicates a network issue or invalid token")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
        print("💡 Check your .env file and bot permissions")

if __name__ == "__main__":
    main()
