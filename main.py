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

FS_URL = "https://local-it.flashscore.ninja/3/x/feed/f_1_0_en_1"
FS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Fsb-Xhr": "f80b5988-d0ed-4d44-a38c-c10f11db0e9a",
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


def to_int(value):
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return int(digits) if digits else 0


def calculate_risk_score(minute, score):
    if minute >= 70 and score == "0-0":
        return 90
    elif minute >= 60:
        return 75
    elif minute >= 45:
        return 60
    return 40


def parse_feed(raw):
    found = {}
    league = "Live League"
    for record in raw.split("~"):
        fields = {}
        for part in record.split("¬"):
            if "÷" in part:
                key, val = part.split("÷", 1)
                fields[key] = val
        if "ZA" in fields:
            league = fields["ZA"]
        if "AA" in fields and fields.get("AB") == "2":
            home = fields.get("AE", "").strip()
            away = fields.get("AF", "").strip()
            if not home or not away:
                continue
            score = f"{to_int(fields.get('AG', 0))}-{to_int(fields.get('AH', 0))}"
            minute = to_int(fields.get("AZ", 0))
            found[(home, away)] = {
                "league": league,
                "home_team": home,
                "away_team": away,
                "status": "LIVE",
                "minute": minute,
                "score": score,
                "match_time": f"{minute}'",
                "risk_score": calculate_risk_score(minute, score),
            }
    return list(found.values())


def fetch_flashscore_live():
    try:
        resp = requests.get(FS_URL, headers=FS_HEADERS, timeout=10)
        if resp.status_code != 200:
            print("Flashscore cavabı:", resp.status_code)
            return []
        matches = parse_feed(resp.text)
        if not matches:
            print("Canlı oyun tapılmadı. Cavabın başı:", resp.text[:200])
        return matches
    except Exception as e:
        print("Flashscore xətası:", e)
        return []


def save_to_supabase(data):
    if not data:
        return
    url = f"{SUPABASE_URL}/rest/v1/matches?on_conflict=home_team,away_team"
    resp = requests.post(url, headers=headers, json=data, timeout=15)
    if resp.status_code in [200, 201, 204]:
        print(f"Uğurlu: {len(data)} canlı oyun Supabase-ə yazıldı!")
    else:
        print("Supabase xətası:", resp.text)


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    print("Canlı Flashscore Scraper işə düşdü...")
    while True:
        try:
            save_to_supabase(fetch_flashscore_live())
        except Exception as e:
            print("Xəta:", e)
        time.sleep(60)
