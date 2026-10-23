import time
import requests

SUPABASE_URL = "https://ncmoxbgwxfkbemurfwan.supabase.co"
SUPABASE_KEY = "sb_publishable_-HUT9l5yw4PZma1B6a2DXg_MPSA0Vwo"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=minimal",
}


def fetch_live_matches():
    # DİQQƏT: bu hissə hələ test məlumatıdır.
    # Real API əlavə edəndə burada onun cavabını oxuyacağıq.
    return [
        {
            "league": "La Liga",
            "home_team": "Real Madrid",
            "away_team": "Barcelona",
            "status": "LIVE",
            "minute": 15,
            "score": "0-0",
            "match_time": "15'",
            "risk_score": 75,
        }
    ]


def save_to_supabase(data):
    if not data:
        print("Göndəriləcək məlumat yoxdur.")
        return
    url = f"{SUPABASE_URL}/rest/v1/matches?on_conflict=home_team,away_team"
    response = requests.post(url, headers=headers, json=data, timeout=15)
    if response.status_code in [200, 201, 204]:
        print("Məlumat Supabase-ə yazıldı!")
    else:
        print("Supabase xətası:", response.text)


if __name__ == "__main__":
    print("Scraper işə düşdü...")
    while True:
        try:
            live_data = fetch_live_matches()
            save_to_supabase(live_data)
        except Exception as e:
            print("Xəta:", e)
        time.sleep(60)
