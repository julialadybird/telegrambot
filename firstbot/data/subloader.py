import os
from ujson import loads
import aiofiles


async def get_json(filename: str) -> list:
    path = f"firstbot/data/{filename}"

    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            # return loads(await file.read())
            content = await file.read()
            return loads(content)
    except Exception as e:
        print(f"Error reading JSON file {filename}: {e}")
        return []


