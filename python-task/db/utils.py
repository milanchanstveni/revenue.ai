from tortoise import Tortoise
from typing import Dict, Any
import asyncio
import aiohttp

from core.env import env
from db.exceptions import (
    InitError,
    CloseError,
    DatabaseError
)
from core.logging import LOG
from core.utils import async_iter
from db.schema import (
    Country,
    PriorityCode
)


db_url = "{}://{}:{}@{}:{}/{}".format(
        env("DB_SCHEME"),
        env("DB_USER"),
        env("DB_PASSWORD"),
        env("DB_HOST"),
        env("DB_PORT"),
        env("DB_NAME"),
)

if env("DEBUG") in ["1", 1, True, "true", "on", "yes"]:
    # db_url = "sqlite:///db.sqlite3"
    db_url = "sqlite://:memory:"


async def create_database() -> None:
    """Connect to the database and create the tables if they don't exist."""
    try:
        await asyncio.sleep(10)
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['db.schema']}
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        LOG.error(f"{e}")
        raise InitError(str(e))


def get_db_config() -> Dict[str, Any]:
    """Get the database configuration."""
    return {
        "connections": {
            "default": db_url
        },
        "apps": {
            "models": {
                "models": ["db.schema", "aerich.models"],
                "default_connection": "default"
            }
        }
    }


CONFIG = get_db_config()


async def close() -> None:
    """Close all database connections."""
    try:
        await Tortoise.close_connections()
    except Exception as e:
        LOG.error(f"{e}")
        raise CloseError(str(e))


async def load_countries() -> None:
    """Store list of countries from external API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://restcountries.com/v3.1/all') as resp:
                data = []
                async for obj in async_iter(await resp.json()):
                    data.append(
                        Country(
                            code=obj['cca2'],
                            name=obj['name']['common'],
                            description=obj['name']['official'],
                            region=obj['continents'][0]
                        )
                    )
                await Country.bulk_create(data)

    except Exception as e:
        LOG.error(f"{e}")
        raise DatabaseError(str(e))


async def load_priority_codes() -> None:
    """Store list of priority codes from hardcoded list."""
    try:
        codes = [
            ('A', 'Immediate release (all users)'),
            ('B', 'Bearer Walk-Through (Navy)'),
            ('C', 'Subscriptions (Mapping)'),
            ('F', 'Allowance (Mapping)'),
            ('G', 'Flight Information Publications and Products (FLIPS) (Mapping)'),
            ('H', 'Hot (Navy)'),
            ('J', 'Disposal Release Order (Mapping) (Process order as free flow bypassing work bench for cycle releases)'),
            ('M', 'Ammunition Transship via Customer Interface Control System (CICS) (Air Force)'),
            ('O', 'Overnight (Navy)'),
            ('P', 'Digital Point Positioning Data Base (DPPB) (Mapping)'),
            ('Q', 'Quick (Navy)'),
            ('R', 'Sectional (Mapping)'),
            ('S', 'Standard Base Supply System (SBSS) Prepositioned Transship (Air Force)'),
            ('T', 'Next Day Delivery (Air Force) (SBSS stock - Relates to Air Force Delivery Priority 7)'),
            ('U', 'Twelve (12) Hour Delivery (Air Force) (Mission Impaired Capability (MIC) Stock Replenishment/Bench Stock - Relates to Air Force Delivery Priority 6)'),
            ('V', 'Eight (8) Hour Delivery (Air Force) (Production Issues - Relates to Air Force Delivery Priority 5)'),
            ('W', 'Four (4) Hour Delivery (Air Force) (Maintenance Line - Relates to Air Force Delivery Priority 4)'),
            ('X', 'One (1) Hour Delivery (Air Force) (Awaiting Parts (AWP)/Work Stoppage - Relates to Air Force Delivery Priority 3), or (Navy) (Navy Request to free flow BRAC Issues)'),
            ('Y', 'Thirty (30) Minute Delivery (Air Force) (Anticipated Mission Impaired Capability Awaiting Parts (MICAP) - Relates to Air Force Delivery Priority 2)'),
            ('Z', 'Thirty (30) Minute Delivery (Air Force) (MICAP - Relates to Air Force Delivery Priority 1)')
        ]        
        data = []
        async for obj in async_iter(codes):
            data.append(
                PriorityCode(
                    code=obj[0],
                    description=obj[1]
                )
            )
        await PriorityCode.bulk_create(data)

    except Exception as e:
        LOG.error(f"{e}")
        raise DatabaseError(str(e))


async def delete_all_country_records() -> None:
    """Delete all country records."""
    try:
        await Country.all().delete()
    except Exception as e:
        LOG.error(f"{e}")
        raise DatabaseError(str(e))


async def delete_all_priority_records() -> None:
    """Delete all priority records."""
    try:
        await PriorityCode.all().delete()
    except Exception as e:
        LOG.error(f"{e}")
        raise DatabaseError(str(e))