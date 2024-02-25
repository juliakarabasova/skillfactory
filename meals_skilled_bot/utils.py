import asyncio
from random import choices

from token_data import MEALS_TOKEN


async def meals_list(session):
    async with session.get(
            url=f'http://www.themealdb.com/api/json/v1/{MEALS_TOKEN}/list.php?c=list',
    ) as resp:
        data = await resp.json()
    return data['meals']


async def collect_recipes(session, category, choice_num):
    async with session.get(
            url=f'https://www.themealdb.com/api/json/v1/{MEALS_TOKEN}/filter.php?c={category}',
    ) as resp:
        data = await resp.json()
        return choices(data['meals'], k=choice_num) if choice_num <= len(data['meals']) else data['meals']


async def get_one_meal(session, id_meal):
    async with session.get(
            url=f'https://www.themealdb.com/api/json/v1/{MEALS_TOKEN}/lookup.php?i={id_meal}',
    ) as resp:
        data = await resp.json()
        return data['meals'][0]


async def gather_recipes(session, meals):
    result = await asyncio.gather(*[get_one_meal(session, item) for item in meals])
    return result
