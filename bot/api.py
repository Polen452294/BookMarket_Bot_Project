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


async def get_my_orders(tg_id: int):
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/bot/orders/my", params={"tg_id": tg_id})
        if r.status_code != 200:
            raise RuntimeError(f"API {r.status_code}: {r.text[:300]}")
        return r.json()


async def admin_list_orders(status: str | None = None):
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    params = {"status": status} if status else None
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/bot/admin/orders", headers=headers, params=params)
        if r.status_code != 200:
            raise RuntimeError(f"Admin API {r.status_code}: {r.text[:300]}")
        return r.json()
    
async def admin_get_notify_info(order_id: int):
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/bot/admin/orders/{order_id}/notify-info", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"Admin API {r.status_code}: {r.text[:300]}")
        return r.json()
    
async def admin_set_order_comment(order_id: int, comment: str):
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    payload = {"comment": comment}

    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.patch(
            f"{API_BASE_URL}/bot/admin/orders/{order_id}/comment",
            json=payload,
            headers=headers,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Admin API {r.status_code}: {r.text[:300]}")

async def admin_stats():
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/bot/admin/stats", headers=headers)
        r.raise_for_status()
        return r.json()


async def admin_cleanup(status: str | None = None, days: int | None = None):
    headers = {"X-Bot-Admin-Token": BOT_ADMIN_TOKEN}
    params = {}
    if status:
        params["status"] = status
    if days:
        params["older_than_days"] = days

    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.delete(f"{API_BASE_URL}/bot/admin/orders/cleanup", headers=headers, params=params)
        r.raise_for_status()
        return r.json()

async def get_order(order_id: int):
    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        r = await client.get(f"{API_BASE_URL}/bot/orders/{order_id}")
        r.raise_for_status()
        return r.json()
