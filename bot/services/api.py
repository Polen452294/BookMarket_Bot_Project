from typing import Any, Dict, List
import aiohttp
from config import API_BASE_URL


async def api_get_json(path: str) -> Any:
    url = f"{API_BASE_URL}{path}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_products() -> List[Dict[str, Any]]:
    return await api_get_json("/products")


async def get_product(product_id: int) -> Dict[str, Any]:
    return await api_get_json(f"/products/{product_id}")