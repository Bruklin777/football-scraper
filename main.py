import requests

SUPABASE_URL = "https://ncmoxbgwxfkbemurfwan.supabase.co"
SUPABASE_KEY = "sb_publishable_-HUT9l5yw4PZma1B6a2DXg_MPSA0Vwo"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

match_data = {
    "league": "Premier League",
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "status": "LIVE",
    "minute": 35,
    "score": "1-0",
    "match_time": "35'",
    "risk_score": 85,
}

url = f"{SUPABASE_URL}/rest/v1/matches"
response = requests.post(url, headers=headers, json=match_data)

if response.status_code in [200, 201]:
    print("Məlumat uğurla yazıldı!")
else:
    print("Xəta:", response.text)
