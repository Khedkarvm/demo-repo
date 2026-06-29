import json
import aiofiles
import os

FILE_PATH = "intern_data.json"

async def read_intern_data():
    if not os.path.exists(FILE_PATH):
        return []

    async with aiofiles.open(FILE_PATH, "r") as f:
        content = await f.read()
        return json.loads(content) if content else []

async def write_intern_data(data):
    async with aiofiles.open(FILE_PATH, "w") as f:
        await f.write(json.dumps(data, indent=4))
