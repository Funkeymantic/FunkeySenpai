import requests

API_BASE_URL = "https://api.callofduty.com"  # Replace with actual API endpoint
API_KEY = "your_cod_api_key"

def get_player_stats(player_id):
    """Fetch player stats for Call of Duty based on player ID."""
    url = f"{API_BASE_URL}/players/{player_id}/stats"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
