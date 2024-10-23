
# FunkeySenpai Bot

**FunkeySenpai Bot** is a multi-functional Discord and Twitch bot designed to manage contests, provide live stream notifications, auto-moderate chats, handle role management via reactions, offer mini-games (like chess), and track user performance in gaming contests. It integrates with multiple platforms, including Discord, Twitch, and APIs of supported games for contest tracking.

## Features
- **Contests**: Create and manage contests with inputs like game, start date, reward, and objective.
- **Mini-Games**: Play games like chess with users or against the bot.
- **Twitch Notifications**: Send live notifications for streamers in the Discord server.
- **Auto-Moderation**: Automatically warn users for inappropriate words in both Twitch and Discord chats, with a mod alert after repeated offenses.
- **Role Management**: Allow users to select roles using reactions and assign roles dynamically based on certain conditions.
- **Cheese Jokes**: Automatically respond with cheese jokes when "cheese" is mentioned in any chat.
- **Private Voice Channels**: Create private voice channels (houses) for users, with commands to manage channel-specific roles.
- **Logging**: Log all actions and punishments in both Discord and Twitch.
- **Custom Commands**: Issue Twitch or Discord commands that communicate between multiple bots running on separate computers.
- **Multi-Server Support**: The bot can be configured to work across multiple Discord servers, with separate configurations for each server stored in a local `config.json` file.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/FunkeySenpai.git
cd FunkeySenpai
```

### 2. Set up Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

The required libraries include:
- `discord.py`
- `requests`
- `python-dotenv`
- `python-chess`
- `aiohttp` (for API handling)

### 4. Environment Setup

Create a `.env` file in the root directory and add your bot tokens and client IDs:

```env
DISCORD_TOKEN=your_discord_bot_token
TWITCH_TOKEN=your_twitch_token
TWITCH_CLIENT_ID=your_twitch_client_id
```

### 5. Run the Bot

```bash
python bot.py
```

## Multi-Server Support Configuration

The bot supports multiple Discord servers, with each server having its own configurations (such as channel IDs, category IDs, and roles). These configurations can be managed directly from Discord by server admins using the following commands:

### Server Configuration Commands
- **Set Default Channel**:
  ```bash
  !set_channel #channel
  ```
  Sets the default channel for bot notifications in the current server.

- **Set Default Category**:
  ```bash
  !set_category #category
  ```
  Sets the default category for bot-created channels in the current server.

- **Set Default Role**:
  ```bash
  !set_role @role
  ```
  Sets the default role to be assigned by the bot in the current server.

- **Show Current Server Configuration**:
  ```bash
  !show_config
  ```
  Displays the current server's configuration for channels, categories, and roles.

These configurations are stored in the local `config.json` file on the machine hosting the bot and are unique to each server the bot is part of.

## How to Update the Bot

### 1. Pull Latest Changes

```bash
git pull origin main
```

### 2. Install New Dependencies (if applicable)

If new dependencies were added:

```bash
pip install -r requirements.txt
```

### 3. Restart the Bot

```bash
# Stop the running bot
Ctrl + C  # On Windows or Linux
Command + C  # On macOS

# Start the bot again
python bot.py
```

## Troubleshooting

- Ensure you have the proper bot permissions (manage roles, send messages, read messages).
- Double-check your `.env` file to confirm the tokens and client IDs are correct.
- Make sure all dependencies are installed correctly by running:

   ```bash
   pip install -r requirements.txt
   ```

If issues persist, feel free to open an issue on GitHub or contact the maintainers.
