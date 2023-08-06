# pyfreedompro

Python library for Freedompro API.

Installation
------------

You can install pyfreedompro with `pip install pyfreedompro`.

Example
-------

```python
import asyncio
import pyfreedompro
import aiohttp

async def main():
    httpsession = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False));
    response = await pyfreedompro.get_list(httpsession, APY_KEY);
    print(response);
    await httpsession.close();
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```


See the complete documentation of the Fredompro API <https://api.freedompro.eu/>.
