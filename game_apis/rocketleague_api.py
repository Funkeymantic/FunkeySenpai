import requests

API_BASE_URL = "https://api.rocketleague.com"
API_KEY = "your_rl_api_key"

def get_player_stats(player_id):
    """Fetch player stats for Rocket League."""
    url = f"{API_BASE_URL}/players/{player_id}/stats"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
