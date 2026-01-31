from __future__ import annotations

import httpx


class TelegramError(Exception):
    def __init__(self, message: str, *, code: int | None = None):
        super().__init__(message)
        self.code = code


async def tg_send_message(token: str, chat_id: int, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.post(url, json={"chat_id": chat_id, "text": text})
        data = r.json()
        if not data.get("ok"):
            desc = data.get("description", "Telegram error")
            code = data.get("error_code")
            raise TelegramError(desc, code=code)
