
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
- **Contests and Game Tracking**: Track game performance through in-game APIs and manage leaderboards.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/FunkeySenpai.git
cd FunkeySenpai
```

### 2. Set up Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
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

## How to Use the FunkeySenpai Bot

### Contests
- **Create a Contest (Mod-Only):**

   ```bash
   !create_contest
   ```

   The bot will ask for the following details:
   - Game (e.g., Valorant)
   - Start date (YYYY-MM-DD)
   - Duration (e.g., 2 weeks)
   - Reward (e.g., Steam gift card)
   - Objective (e.g., most kills)
   - Group (followers, subscribers, or both)
   - Rules (comma-separated)

- **Join a Contest:**

   Users can join a contest using the `~contest` command followed by their player ID:

   ```bash
   ~contest player_id
   ```

- **List Contests:**

   ```bash
   !list_contests
   ```

- **List Participants (Mod-Only):**

   ```bash
   !list_participants contest_id
   ```

### Twitch Notifications
- Automatically send live notifications to Discord when users with the "streamer" role go live.
  
### Auto-Moderation
- **Auto-warn for bad words**: If a user uses certain words, the bot issues warnings. After two warnings, the bot alerts mods in a dedicated mod channel and deletes the message.
  
### Role Management
- **Setup Reaction Roles (Mod-Only):**

   Use the command to set up a message for users to react to for role assignment:

   ```bash
   !setup_reaction_roles
   ```

   The bot will guide you through:
   - Adding emoji-role pairs
   - Setting whether users can select multiple roles
   - Publishing the reaction message in a chosen channel
  
### Mini-Games
- **Play Chess:**

   Start a chess game against a bot or another user:

   ```bash
   !chess_start [@opponent]
   ```

   Make a move using UCI format:

   ```bash
   !chess_move e2e4
   ```

### Custom Commands
- **Manage Private Voice Channels (House System)**: Mods and users can manage private voice channels with commands to create, assign, and manage roles:
   - `!create_house <house_name>`
   - `!give_key @user`
   - `!take_key @user`

### Cheese Jokes
- Whenever "cheese" is mentioned in any chat, the bot will respond with a cheese joke.

## Logging
All actions (warnings, bans, role changes) are logged to the console and can be tracked in the mod chat.

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

## How to Start the Bot

1. **Activate the virtual environment:**

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the bot:**

   ```bash
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
