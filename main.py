import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

SUPABASE_URL = "https://ncmoxbgwxfkbemurfwan.supabase.co"
SUPABASE_KEY = "sb_publishable_-HUT9l5yw4PZma1B6a2DXg_MPSA0Vwo"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=minimal",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


def fetch_live_matches():
    # Hələ test məlumatıdır. Sonra real API qoşacağıq.
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
    threading.Thread(target=run_server, daemon=True).start()
    print("Scraper işə düşdü...")
    while True:
        try:
            live_data = fetch_live_matches()
            save_to_supabase(live_data)
        except Exception as e:
            print("Xəta:", e)
        time.sleep(60)
