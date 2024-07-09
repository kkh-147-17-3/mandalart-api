from datetime import datetime

import requests


def send_discord_notification(content: str):
    url = "https://discord.com/api/webhooks/..."
    return requests.post(url, data={"content": content})


def check_health(base_url, port=80):
    current_date = datetime.now()
    url = f"{base_url}:{port}"
    message = ""
    try:
        res = requests.get(url)
        if res.status_code != 200:
            message = f"[{current_date}]Internal Server Error: {res}"

        if res.status_code == 200:
            message = f"[{current_date}]({res.json()})Server is running"
        send_discord_notification(message)
        return res.json()['flag']

    except Exception as e:
        message = f"Server health-check failed {e} - {current_date}"
        send_discord_notification(message)
        raise e
