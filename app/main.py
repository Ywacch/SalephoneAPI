import asyncpg.exceptions
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from sqlalchemy import func
import asyncio
from app.log import fastapi_log, app_log

from app.database.db import database
from app.database.db import tables
#from app.cache.redis_cache import RedisCache


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods=["*"],
    allow_headers=["*"]
)

smartphones = tables.Smartphones.__table__


async def start_scheduler():
    """
    Background task to update the cache every 24 hours
    :return:
    """

    while True:
        await asyncio.sleep(24*60*60)
        app_log.info("Scheduled cache update.....")
        asyncio.create_task(app.redis.update_cache(database))
        app_log.info("Scheduled cache update Finished!")


@app.on_event("startup")
async def startup():
    """
    On startup, initialize the db connection and populate the cache with pre-computed price history
    :return:
    """
    await database.connect()
    #app.redis = RedisCache()
    #asyncio.create_task(app.redis.update_cache(database))
    #asyncio.create_task(start_scheduler())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    #await app.redis.close_redis()


@app.get("/phones/")
async def all_phones(detailed: Union[bool, None] = None, brand: Union[str, None] = None, series: Union[str, None] = None):

    query = smartphones.select
    filters = []

    if series and not brand:
        error_message = f"'series' parameter requires a provided 'brand' parameter"
        raise HTTPException(status_code=400, detail=error_message)

    if brand:
        filters.append(func.lower(smartphones.c.brand) == brand.lower())

    if series:
        filters.append(func.lower(smartphones.c.series) == series.lower())

    if detailed:
        phones = await database.fetch_all(query=query().filter(*filters))
    else:
        phones = await database.fetch_all(query=query().filter(*filters)
                                          .with_only_columns(smartphones.c.phone_id, smartphones.c.phone_name))
    return phones


@app.get("/phones/brands")
async def phone_brands():
    phones = await database.fetch_all(query=smartphones.select()
                                      .with_only_columns(smartphones.c.brand).distinct())
    return {"brands": [brand['brand'] for brand in phones]}


@app.get("/phones/series")
async def phone_series(brand: str):
    phones = await database.fetch_all(query=smartphones.select().filter(func.lower(smartphones.c.brand) == brand.lower())
                                      .with_only_columns(smartphones.c.series).distinct())
    return {"series": [serie['series'] for serie in phones]}


@app.get("/phones/{_id}")
async def phone_id(_id: str, detailed: Union[bool, None] = None):
    if detailed:
        phone = await database.fetch_one(query=smartphones.select().filter(smartphones.c.phone_id == _id))
    else:
        phone = await database.fetch_one(query=smartphones.select().filter(smartphones.c.phone_id == _id)
                                         .with_only_columns(smartphones.c.phone_id, smartphones.c.phone_name))
    if not phone:
        raise HTTPException(status_code=404, detail="Item not found")
    return phone


@app.get("/phones/{_id}/price_history")
async def price_history(_id: str, timeframe: str = "day"):
    result = []
    query = f"""select date_trunc(:timeframe, converted_listings.date_added)as datetime, brand, series,
            model, storage_size,
            round(avg(converted_listings.price)::decimal, 1 ) as average from (select * from phonelistings inner join 
            smartphones on smartphones.phone_id=phonelistings.phone_id where smartphones.phone_id = 
            :id ) sub inner join (select  item_id, title, date_added, 
            canadian_price_base as price from listings) as converted_listings on 
            converted_listings.item_id=sub.item_id AND converted_listings.date_added=sub.date_added group by 
            datetime, brand, series, model, storage_size order by datetime;"""

    # Try to get the data from the cache, if it's not there look in the database
    try:
        if timeframe == 'day':  # only the daily frequency is cached
            result = None # await app.redis.get(_id)
    except Exception as e:
        fastapi_log.error(e)
    else:
        if not result:
            app_log.info("Caching failed, querying database ....")
            try: # TODO: add the data fetched from the database to the cache
                result = await database.fetch_all(query=query, values={"timeframe": timeframe, "id": _id})
            except asyncpg.exceptions.InvalidParameterValueError:
                error_message = f"timestamp '{timeframe}' is not a valid parameter"
                raise HTTPException(status_code=400, detail=error_message)
            else:
                if not result:
                    raise HTTPException(status_code=404, detail="Item not found")
    return result
