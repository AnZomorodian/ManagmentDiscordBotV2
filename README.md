
# 🤖 Amazing Management Bot v3.0

> **A powerful, modular Discord bot with advanced voice channel management, moderation tools, and smart automation features.**

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-blue.svg)](https://discordpy.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Replit](https://img.shields.io/badge/Hosted%20on-Replit-orange.svg)](https://replit.com)

## ✨ Features

### 🎵 Smart Voice Management
- **Auto Voice Channels**: Creates temporary voice channels when users join trigger channels
- **Intelligent Bitrate**: Automatically adjusts quality based on server boost level
- **User Limits**: Configurable per-user channel creation limits
- **Auto-Cleanup**: Channels delete themselves when empty

### 🛡️ Advanced Moderation
- **Message Purging**: Bulk delete messages with admin controls
- **User Management**: Kick, ban, and timeout members
- **Auto-Role Assignment**: Welcome new members with automatic roles
- **Moderation Logging**: Track all admin actions

### 🎉 Welcome System
- **Custom Welcome Messages**: Greet new members with styled embeds
- **Member Counter**: Track server growth
- **Channel-Specific Welcomes**: Route messages to designated channels

### 📊 Statistics & Analytics
- **Server Analytics**: Detailed server information and statistics
- **Bot Performance**: Real-time bot metrics and latency
- **User Statistics**: Track individual member activity
- **Channel Usage**: Monitor voice channel creation patterns

### 🎨 Enhanced User Experience
- **Rich Embeds**: Beautiful, color-coded message formatting
- **Status Rotation**: Dynamic bot status messages
- **Error Handling**: User-friendly error messages with suggestions
- **Modular Architecture**: Clean, maintainable code structure

## 🚀 Quick Start

### 1. Bot Setup
1. Visit the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy your bot token
4. Add the token as a secret named `TOKEN` in Replit's Secrets tab

### 2. Bot Permissions
Invite your bot with these permissions:
- **Administrator** (recommended for full functionality)
- Or individual permissions:
  - Manage Channels
  - Manage Messages
  - Manage Roles
  - View Channels
  - Send Messages
  - Embed Links
  - Connect/Speak in Voice Channels

### 3. Run the Bot
Simply click the **Run** button in Replit, or use:
```bash
python main.py
```

## 🎮 Commands

### 👑 Administrator Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!setup` | Complete bot configuration | `!setup` |
| `!setwelcome` | Set welcome channel | `!setwelcome #general` |
| `!setlogs` | Set logging channel | `!setlogs #logs` |
| `!settrigger` | Set voice trigger channel | `!settrigger #join-to-create` |
| `!voicesettings` | Configure voice options | `!voicesettings` |

### 🛡️ Moderation Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!purge` | Delete multiple messages | `!purge 10` |
| `!kick` | Kick a member | `!kick @user reason` |
| `!ban` | Ban a member | `!ban @user reason` |
| `!mute` | Timeout a member | `!mute @user 10m` |

### 📊 Information Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!help` | Show all commands | `!help` |
| `!serverinfo` | Server statistics | `!serverinfo` |
| `!botstats` | Bot performance metrics | `!botstats` |
| `!mystats` | Your personal statistics | `!mystats` |

### 🎪 Fun Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!ping` | Check bot responsiveness | `!ping` |
| `!roll` | Roll dice | `!roll 6` or `!roll 2d20` |
| `!8ball` | Magic 8-ball responses | `!8ball Will it rain?` |
| `!flip` | Flip a coin | `!flip` |

## ⚙️ Configuration

### Voice Channel Settings
- **Quality Levels**: Automatic bitrate adjustment (Standard: 64kbps, High: 128kbps, Premium: 256kbps+)
- **User Limits**: Maximum channels per user (default: 3)
- **Auto-Delete**: Channels remove themselves when empty (5 minutes timeout)
- **Trigger Channels**: Specific channels that create new voice rooms

### Moderation Features
- **Welcome Messages**: Customizable greeting system
- **Auto-Roles**: Automatically assign roles to new members
- **Logging**: Track all moderation actions
- **Banned Words**: Content filtering (coming soon)

## 🏗️ Architecture

```
├── config/          # Bot configuration and settings
│   ├── settings.py  # Main configuration file
│   └── __init__.py
├── handlers/        # Command and event handlers
│   ├── admin_commands.py     # Administrator commands
│   ├── commands.py           # Command registration
│   ├── events.py             # Discord event handlers
│   ├── fun_commands.py       # Entertainment commands
│   ├── info_commands.py      # Information commands
│   ├── moderation_commands.py # Moderation tools
│   └── __init__.py
├── utils/           # Utility functions and helpers
│   ├── database.py  # Data storage management
│   ├── helpers.py   # Helper functions
│   └── __init__.py
└── main.py          # Bot entry point
```

## 🎨 Customization

### Adding New Commands
1. Create your command function in the appropriate handler file
2. Register it in `handlers/commands.py`
3. The bot will automatically load it on restart

### Custom Embed Colors
Modify the `COLORS` dictionary in `utils/helpers.py`:
```python
COLORS = {
    "success": 0x00ff00,
    "error": 0xff0000,
    "warning": 0xffff00,
    "info": 0x00ffff,
    "admin": 0xff00ff
}
```

### Voice Channel Names
Customize channel naming templates in `config/settings.py`:
```python
CHANNEL_NAMES = [
    "{}'s Room",
    "{}'s Hangout",
    "{}'s Voice Chat"
]
```

## 🔧 Troubleshooting

### Common Issues

**❌ 429 Too Many Requests Error**
- Wait 5-10 minutes before restarting
- Check rate limiting in Discord API

**❌ Missing Permissions**
- Ensure bot has Administrator permission
- Check channel-specific permissions

**❌ Voice Channels Not Creating**
- Verify trigger channels are set with `!settrigger`
- Check bot has "Manage Channels" permission
- Ensure user isn't at channel limit

**❌ Commands Not Working**
- Check bot has "Send Messages" permission
- Verify command prefix is correct (`!`)
- Try `!help` to see available commands

### Getting Help
1. Use `!botstats` to check bot status
2. Check the console for error messages
3. Verify all permissions are correctly set
4. Ensure your token is valid and in Secrets

## 🔄 Version History

### v3.0 - Modular Architecture Update
- ✅ Separated code into organized modules
- ✅ Fixed voice channel bitrate compatibility issues
- ✅ Enhanced error handling and user feedback
- ✅ Improved performance and stability
- ✅ Better code organization and maintainability
- ✅ Added comprehensive logging system

### v2.x - Feature Expansion
- Added moderation commands
- Implemented user statistics
- Enhanced welcome system

### v1.x - Initial Release
- Basic voice channel management
- Simple command system

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features  
- Submit pull requests
- Improve documentation

## 🔗 Links

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Bot Setup Guide](https://discordpy.readthedocs.io/en/stable/discord.html)

---

*Built with ❤️ using Python and discord.py | Hosted on Replit*
