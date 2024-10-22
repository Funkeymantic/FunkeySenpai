import requests
import os

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')

def get_streamer_status(username):
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_TOKEN}'
    }
    response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={username}', headers=headers)
    return response.json()
