import os
import json
import time
import urllib.request
import urllib.parse

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Telegram Bot Token is missing")

API = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text):
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text
    }).encode()

    urllib.request.urlopen(
        API + "sendMessage",
        data=data
    )

def main():
    offset = 0

    print("Quotex Signal Bot Started!")

    while True:
        try:
            url = API + "getUpdates?offset=" + str(offset)

            response = urllib.request.urlopen(url)
            updates = json.loads(response.read())

            for update in updates.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                command = message.get("text", "")

                if not chat_id:
                    continue

                if command == "/start":
                    send_message(
                        chat_id,
                        "Welcome to Quotex Signal Bot! 🚀\n\n"
                        "Commands:\n"
                        "/signal - Check signal status\n"
                        "/help - Help"
                    )

                elif command == "/signal":
                    send_message(
                        chat_id,
                        "Signal system is being configured.\n"
                        "Real market data is not connected yet.\n"
                        "No unverified signals will be provided."
                    )

                elif command == "/help":
                    send_message(
                        chat_id,
                        "Quotex Signal Bot Help\n"
                        "/start\n/signal\n/help"
                    )

        except Exception as error:
            print("Error:", error)
            time.sleep(5)

if __name__ == "__main__":
    main()
