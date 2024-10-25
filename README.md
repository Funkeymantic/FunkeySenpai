
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

## Setup Instructions

### 1. Clone the Repository

Open a terminal or command prompt, then run:

```bash
git clone https://github.com/your-username/FunkeySenpai.git
cd FunkeySenpai
```

### 2. Set up Virtual Environment

To keep dependencies isolated, create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Dependencies

Install the necessary libraries by running:

```bash
pip install -r requirements.txt
```

The required libraries include:
- `discord.py`
- `requests`
- `python-dotenv`
- `python-chess`
- `aiohttp`
- `schedule`

### 4. Environment Setup

Create a `.env` file in the root directory to store your bot’s credentials. This file should look like:

```env
DISCORD_TOKEN=your_discord_bot_token
TWITCH_TOKEN=your_twitch_token
TWITCH_CLIENT_ID=your_twitch_client_id
```

Replace the placeholders with your actual Discord bot token and Twitch API credentials.

### 5. Run the Bot

To run the bot, use the following command in the terminal:

```bash
python bot.py
```

Make sure the bot starts without any errors.

## Automatic GitHub Update at 5:00 AM

The bot is now configured to automatically check the time and pull updates from GitHub at 5:00 AM daily. It will restart itself after pulling the updates.

### Testing Automatic GitHub Updates

To test this feature:
- Set your system's time or modify the `pull_and_restart()` function temporarily to trigger at a closer time for testing.
- Ensure that the GitHub repository is up to date.

## Configuring for Multiple Servers

The bot supports multiple Discord servers, each with its own unique configurations (such as channel IDs, category IDs, and roles). These configurations are stored in a local `config.json` file and can be managed directly within Discord using the following commands:

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

The `config.json` file is generated automatically when you configure your server and will be updated when you run any of these commands.

## Updating the Bot

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

- Ensure you have the correct permissions set for the bot (manage roles, send messages, read messages).
- Verify that the `.env` file contains valid credentials for both Discord and Twitch.
- Ensure that all dependencies are installed by running:

   ```bash
   pip install -r requirements.txt
   ```

If issues persist, feel free to open an issue on GitHub or contact the maintainers for support.
