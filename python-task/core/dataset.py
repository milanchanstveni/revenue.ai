import datetime
from typing import (
    BinaryIO,
    Tuple,
    List,
    Union,
    Any
)
import pandas as pd
import asyncio
import aiohttp

from core.logging import LOG
from core.utils import async_iter
from core.env import env


def read_file(file_data: BinaryIO) -> Union[pd.DataFrame, None]:
    try:
        df = pd.read_csv(file_data)
    except pd.errors.ParserError:
        try:
            df = pd.read_excel(file_data)
        except Exception as e:
            LOG.error(f"Invalid file format provided: {e}")
            raise Exception("Invalid file format provided") from e
    return df


async def call_api1(country: str, region: str) -> bool:
    try:
        credentials = aiohttp.BasicAuth(env('AUTH_USER'), env('AUTH_PASS'))
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api1:5000/MasterData/Country?countryName={country}', auth=credentials) as resp:
                if len(await resp.json()) == 0:
                    async with session.get('http://api1:5000/MasterData/Country', auth=credentials) as resp1:
                            resp = resp1

                async for c in async_iter(await resp.json()):
                    if c['region'] == region and c['name'] == country:
                        return True
        
        return False

    except Exception as E:
        LOG.info(str(E))
        return False


async def call_api2(code: str) -> bool:
    try:
        credentials = aiohttp.BasicAuth(env('AUTH_USER'), env('AUTH_PASS'))
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api2:5001/{code}', auth=credentials) as resp:
                return True if await resp.text() in [1, "1", "'1'", '"1"'] else False        
        
    except Exception as E:
        LOG.info(str(E))
        return False


async def validate(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    valid = []
    invalid = []

    async for i in async_iter(dataset.iterrows()):
        _, row = i

        if not await call_api1(row['Country'], row['Region']):
            invalid.append(
                f"Invalid region and country combination: {row['Country']}/{row['Region']}"
            )
            continue

        if not await call_api2(row['Order Priority']):
            invalid.append(
                f"Invalid order priority value({row['Order Priority']}) for {row['Country']}"
            )
            continue

        if row['Total Profit'] < 1000:
            invalid.append(
                f"Total Profit is less than 1000({row['Total Profit']}) for {row['Country']}"
            )
            continue

        if row['Total Cost'] > 5000000:
            invalid.append(
                f"Total Cost is greater than 5000000({row['Total Cost']}) for {row['Country']}"
            )
            continue

        order_date = datetime.datetime.strptime(row['Order Date'], '%m/%d/%Y')
        ship_date = datetime.datetime.strptime(row['Ship Date'], '%m/%d/%Y')
        if order_date >= ship_date:
            invalid.append(
                f"Order Date is not less than Ship Date"
            )
            continue

        if row['Units Sold'] * row['Unit Price'] != row['Total Revenue']:
            invalid.append(
                f"Incorrect Total Revenue calculation for {row['Country']}."
            )
            continue

        if row['Units Sold'] * row['Unit Cost'] != row['Total Cost']:
            invalid.append(
                f"Incorrect Total Cost calculation for {row['Country']}"
            )
            continue

        
        valid.append(row)
    
    valid = pd.DataFrame(valid)

    return (valid, invalid)


def validate_dataset(dataset: pd.DataFrame) -> Tuple[List, List]:
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    results = loop.run_until_complete(validate(dataset))
    loop.close()
    return results

