
# 🤖 Amazing Discord Management Bot v3.1

![Discord.py](https://img.shields.io/badge/discord.py-2.3.2+-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Security](https://img.shields.io/badge/security-.env%20protected-red.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A **powerful**, **secure**, and **feature-rich** Discord bot built with modular architecture and enhanced security using `.env` configuration. Perfect for server management, moderation, and community engagement!

## ✨ Key Features

### 🔐 Enhanced Security
- **Environment Variables**: Secure token storage using `.env` files
- **Token Validation**: Automatic token format verification
- **Permission Checking**: Role-based command access control
- **Rate Limiting**: Built-in protection against spam and abuse

### 🎵 Smart Voice Management
- **Auto Voice Channels**: Create temporary voice rooms on demand
- **Quality Control**: Automatic bitrate adjustment (64kbps to 256kbps+)
- **User Limits**: Configurable channel capacity and per-user limits
- **Auto Cleanup**: Channels automatically delete when empty (5min timeout)
- **Trigger Channels**: Designated channels for voice room creation

### 🛡️ Advanced Moderation
- **Message Management**: Bulk delete, content filtering
- **Member Actions**: Kick, ban, timeout with logging
- **Auto Moderation**: Welcome messages, auto-roles, banned words
- **Audit Logging**: Complete action tracking and reporting

### 📊 Comprehensive Statistics
- **Server Analytics**: Member count, channel stats, activity metrics
- **Bot Performance**: Uptime, latency, command usage tracking
- **User Statistics**: Personal activity tracking and achievements

### 🎪 Entertainment & Engagement
- **Interactive Games**: Dice rolling, coin flipping, Magic 8-Ball
- **Dynamic Responses**: Context-aware replies and reactions
- **Custom Commands**: Extensible command system with aliases

### 🏗️ Modern Architecture
- **Modular Design**: Organized, maintainable code structure
- **Async Performance**: Non-blocking operations for optimal speed
- **Error Handling**: Comprehensive error catching and user feedback
- **Hot Reloading**: Easy updates without full restarts

## 🚀 Quick Setup Guide

### 1. Environment Configuration

Create a `.env` file in your project root:

```env
# Required: Your Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Optional: Additional settings
BOT_PREFIX=!
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### 2. Discord Bot Setup

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy your bot token and add it to your `.env` file
4. **Important**: Keep your token secure and never share it!

### 3. Bot Permissions

Invite your bot with these essential permissions:
- **Administrator** (recommended for full functionality)
- Or specific permissions:
  - `Manage Channels` - For voice channel creation
  - `Manage Messages` - For moderation commands
  - `Manage Roles` - For auto-role features
  - `Connect` & `Speak` - For voice functionality
  - `Send Messages` & `Embed Links` - For basic operation

### 4. Installation & Launch

The bot will automatically install required dependencies. Simply click **Run** or use:

```bash
python main.py
```

## 🎮 Command Reference

### 👑 Administrator Commands
| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!setup` | Complete bot configuration wizard | `!setup` | Administrator |
| `!setwelcome` | Configure welcome channel | `!setwelcome #general` | Manage Guild |
| `!setlogs` | Set moderation log channel | `!setlogs #mod-logs` | Manage Guild |
| `!settrigger` | Configure voice trigger channels | `!settrigger #join-to-create` | Manage Channels |
| `!voicesettings` | Voice channel configuration | `!voicesettings` | Manage Channels |
| `!autorole` | Set auto-role for new members | `!autorole @Member` | Manage Roles |

### 🛡️ Moderation Commands
| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!purge` | Bulk delete messages | `!purge 10` | Manage Messages |
| `!kick` | Remove member from server | `!kick @user reason` | Kick Members |
| `!ban` | Permanently ban member | `!ban @user reason` | Ban Members |
| `!mute` | Timeout member | `!mute @user 10m reason` | Moderate Members |
| `!warn` | Issue warning to member | `!warn @user reason` | Manage Messages |

### 📊 Information Commands
| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!help` | Display all available commands | `!help` | Send Messages |
| `!serverinfo` | Comprehensive server statistics | `!serverinfo` | Send Messages |
| `!botstats` | Bot performance metrics | `!botstats` | Send Messages |
| `!mystats` | Personal activity statistics | `!mystats` | Send Messages |
| `!userinfo` | Detailed user information | `!userinfo @user` | Send Messages |

### 🎪 Fun & Entertainment
| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!ping` | Check bot responsiveness | `!ping` | Send Messages |
| `!roll` | Roll dice (supports multiple dice) | `!roll 6` or `!roll 2d20` | Send Messages |
| `!8ball` | Magic 8-ball predictions | `!8ball Will it work?` | Send Messages |
| `!flip` | Flip a coin | `!flip` | Send Messages |
| `!choose` | Random choice from options | `!choose pizza pasta salad` | Send Messages |

## ⚙️ Advanced Configuration

### Voice Channel Settings
```python
VOICE_SETTINGS = {
    "VOICE_QUALITY_LEVELS": {
        "standard": 64000,    # 64kbps - Basic quality
        "high": 128000,       # 128kbps - High quality  
        "premium": 256000     # 256kbps+ - Premium quality
    },
    "DEFAULT_USER_LIMIT": 0,        # 0 = unlimited
    "AUTO_DELETE_TIMEOUT": 300,     # 5 minutes
    "MAX_CHANNELS_PER_USER": 3      # Per-user channel limit
}
```

### Custom Channel Names
```python
CHANNEL_NAMES = [
    "{}'s Room",
    "{}'s Hangout", 
    "🎵 {}'s Music Room",
    "🎮 {}'s Gaming Room",
    "💬 {}'s Chat Room"
]
```

### Embed Color Scheme
```python
COLORS = {
    "success": 0x00ff00,    # Green
    "error": 0xff0000,      # Red
    "warning": 0xffff00,    # Yellow
    "info": 0x00ffff,       # Cyan
    "admin": 0xff00ff       # Magenta
}
```

## 🔧 Troubleshooting

### Common Issues

**❌ "DISCORD_TOKEN not found" Error**
- Ensure your `.env` file exists in the project root
- Verify `DISCORD_TOKEN=your_token_here` is correctly formatted
- Check that your token is valid and not expired

**❌ "discord module not found" Error**
- The bot will auto-install dependencies on first run
- If issues persist, restart the Repl

**❌ Missing Permissions Error**
- Verify bot has required permissions in your server
- Check that bot role is positioned above roles it needs to manage
- Ensure bot has access to the channels you're using

**❌ Voice Channels Not Creating**
- Use `!settrigger #channel` to configure trigger channels
- Verify bot has "Manage Channels" permission
- Check that users haven't reached their channel limit (default: 3)

**❌ Commands Not Responding**
- Verify bot has "Send Messages" permission
- Check the command prefix (default: `!`)
- Try `!ping` to test basic connectivity

### Getting Support

1. Use `!botstats` to check bot health and performance
2. Check console output for detailed error messages
3. Verify all permissions are correctly configured
4. Ensure your `.env` file is properly formatted

## 🏗️ Project Structure

```
├── config/                    # Configuration and settings
│   ├── settings.py           # Main configuration with .env support
│   └── __init__.py
├── handlers/                 # Command and event handlers
│   ├── admin_commands.py     # Administrator commands
│   ├── commands.py           # Command registration system
│   ├── events.py             # Discord event handlers
│   ├── fun_commands.py       # Entertainment commands
│   ├── info_commands.py      # Information and statistics
│   ├── moderation_commands.py # Moderation tools
│   └── __init__.py
├── utils/                    # Utility functions
│   ├── database.py          # Data storage and management
│   ├── helpers.py           # Helper functions and decorators
│   └── __init__.py
├── .env                     # Environment variables (create this!)
├── .gitignore              # Git ignore file
├── main.py                 # Bot entry point
├── README.md               # This file
└── pyproject.toml          # Python dependencies
```

## 🔄 Version History

### v3.1 - Security & Environment Enhancement
- ✅ **Secure .env Configuration**: Token protection via environment variables
- ✅ **Enhanced Token Validation**: Automatic format verification
- ✅ **Improved Error Handling**: Better user feedback and debugging
- ✅ **Security Hardening**: Rate limiting and permission validation
- ✅ **Performance Optimization**: Faster startup and response times

### v3.0 - Modular Architecture
- ✅ Separated code into organized modules
- ✅ Fixed voice channel bitrate compatibility
- ✅ Enhanced error handling and user feedback
- ✅ Improved performance and stability
- ✅ Better code organization and maintainability

### v2.x - Feature Expansion
- ✅ Advanced moderation commands
- ✅ User statistics and tracking
- ✅ Enhanced welcome system

### v1.x - Initial Release
- ✅ Basic voice channel management
- ✅ Simple command system

## 🔒 Security Best Practices

1. **Never commit your `.env` file** to version control
2. **Regularly rotate your bot token** if compromised
3. **Use least-privilege permissions** when possible
4. **Monitor bot activity** through logs and statistics
5. **Keep dependencies updated** for security patches

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- 🐛 Report bugs and issues
- 💡 Suggest new features and improvements
- 🔧 Submit pull requests
- 📚 Improve documentation
- ⭐ Star the project if you find it helpful!

## 🔗 Useful Links

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)
- [Python dotenv Documentation](https://pypi.org/project/python-dotenv/)

---

**Made with ❤️ by the Amazing Bot Team | Powered by Discord.py and secure .env configuration**
