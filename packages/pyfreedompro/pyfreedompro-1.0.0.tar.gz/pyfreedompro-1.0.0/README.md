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

async def main():
    response = await pyfreedompro.get_list(API_KEY);
    print(response);
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


See the complete documentation of the Fredompro API <https://api.freedompro.eu/>.
