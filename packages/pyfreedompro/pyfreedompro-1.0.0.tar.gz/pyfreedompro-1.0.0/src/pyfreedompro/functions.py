import aiohttp
import asyncio
import async_timeout

FREEDOMPRO_URL = "https://api.freedompro.eu/api/freedompro/accessories"

async def get_list(apikey):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        httpsession = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        with async_timeout.timeout(10000):
            resp = await httpsession.get(FREEDOMPRO_URL, headers=headers)
            status = resp.status

            if status == 200:
                devices = await resp.json()
                await httpsession.close()
                return {"state": True, "devices": devices}

            if status == 401:
                await httpsession.close()
                return {"state": False, "code": -201}

            await httpsession.close()
            return {"state": False, "code": -200}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        await httpsession.close()
        return {"state": False, "code": -200}

async def get_states(apikey):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        httpsession = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        with async_timeout.timeout(10000):
            resp = await httpsession.get(f"{FREEDOMPRO_URL}/state", headers=headers)
            status = resp.status
            if status == 200:
                data = await resp.json()
                await httpsession.close()
                return data
            await httpsession.close()
            return []
    except (asyncio.TimeoutError, aiohttp.ClientError):
        await httpsession.close()
        return []


async def put_state(apikey, uid, payload):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        httpsession = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        with async_timeout.timeout(10000):
            resp = await httpsession.put(
                f"{FREEDOMPRO_URL}/{uid}/state", data=payload, headers=headers
            )
            status = resp.status
            if status == 200:
                data = await resp.json()
                if "state" in data:
                    await httpsession.close()
                    return data["state"]
            await httpsession.close()
            return {}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        await httpsession.close()
        return {}
