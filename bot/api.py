import httpx
from config import API_BASE_URL, BOT_ADMIN_TOKEN


async def upsert_user(tg_id: int, username: str | None, first_name: str | None, source: str | None):
    payload = {"tg_id": tg_id, "username": username, "first_name": first_name, "source": source}
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        await client.post(f"{API_BASE_URL}/bot/users/upsert", json=payload)


async def get_products():
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/products")
        if r.status_code != 200:
            raise RuntimeError(f"API {r.status_code}: {r.text[:300]}")
        return r.json()


async def create_order(tg_id: int, text: str, phone: str | None):
    payload = {"tg_id": tg_id, "text": text, "phone": phone}
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.post(f"{API_BASE_URL}/bot/orders", json=payload)
        return r.status_code, r.text, (r.json() if r.headers.get("content-type", "").startswith("application/json") else None)


async def admin_set_order_status(order_id: int, status: str):
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.patch(f"{API_BASE_URL}/bot/admin/orders/{order_id}/status", json={"status": status}, headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"Admin API {r.status_code}: {r.text[:300]}")
        return r.json()
