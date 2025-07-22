import os
import discord
from discord.ext import commands
import asyncio
from config.settings import TOKEN, PREFIXES, INTENTS
from handlers.events import setup_events
from handlers.commands import setup_commands
from utils.database import initialize_data
from utils.helpers import setup_bot_status

# Initialize bot
bot = commands.Bot(command_prefix=PREFIXES, intents=INTENTS, help_command=None)

# Initialize data storage
initialize_data()

def main():
    """Main bot startup function"""
    try:
        print("🚀 Starting Amazing Management Bot v3.0...")
        print("🔑 Using embedded token...")
        print("👑 Admin features enabled...")
        print("🎵 Smart voice trigger system ready...")
        print("📁 Modular architecture loaded...")

        # Setup event handlers
        setup_events(bot)

        # Setup command handlers
        setup_commands(bot)

        # Setup status rotation
        setup_bot_status(bot)

        # Run the bot
        bot.run(TOKEN)

    except discord.HTTPException as e:
        if e.status == 429:
            print("❌ Rate limited! Too many requests to Discord API")
            print("💡 Wait a few minutes and try again")
        else:
            print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")

if __name__ == "__main__":
    main()