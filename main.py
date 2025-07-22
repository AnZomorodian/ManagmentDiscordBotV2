import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from config.settings import TOKEN, PREFIXES, INTENTS, BOT_VERSION
from handlers.events import setup_events
from handlers.commands import setup_commands
from utils.helpers import setup_bot_status, validate_environment

# Load environment variables
load_dotenv()

# Bot initialization
bot = commands.Bot(
    command_prefix=PREFIXES, 
    intents=INTENTS, 
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    description=f"Amazing Discord Management Bot v{BOT_VERSION}"
)

@bot.event
async def on_ready():
    """Bot ready event"""
    print("=" * 60)
    print(f"🎉 {bot.user.name} is now ONLINE!")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} server(s)")
    print(f"👥 Serving {sum(guild.member_count for guild in bot.guilds)} members")
    print(f"📡 Latency: {round(bot.latency * 1000)}ms")
    print("=" * 60)

async def main():
    """Main bot function"""
    try:
        print("🚀 Starting Amazing Management Bot v3.1...")
        print("🔐 Loading secure .env configuration...")

        # Validate environment
        if not validate_environment():
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

        # Setup status rotation
        asyncio.create_task(setup_bot_status(bot))
        print("✅ Status rotation configured")

        print("🌟 All systems ready! Starting bot...")

        # Run the bot
        await bot.start(TOKEN)

    except discord.LoginFailure:
        print("❌ Login Error: Invalid Discord token!")
        print("💡 Please check your DISCORD_TOKEN in the .env file")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())