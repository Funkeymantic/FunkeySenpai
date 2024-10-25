import requests

API_BASE_URL = "https://api.riotgames.com/val"  # Replace with actual API endpoint
API_KEY = "your_riot_api_key"  # Add your Riot API key here

def get_player_stats(player_id):
    """Fetch player stats for Valorant based on player ID."""
    url = f"{API_BASE_URL}/players/{player_id}/stats"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
