import os
import aioredis
import json
from fastapi.encoders import jsonable_encoder

from app.database import tables
from app.log import app_log


class RedisCache:

    def __init__(self):
        redis_url = f'redis://{os.environ["REDIS_HOST"]}:{os.environ["REDIS_PORT"]}'
        try:
            self.instance = aioredis.from_url(redis_url, password=os.environ['REDIS_PASSWORD'])
        except Exception as e:
            app_log.error(e)

    async def set(self, key, value):
        value = json.dumps(jsonable_encoder(value))
        try:
            await self.instance.set(key, value)
        except Exception as e:
            app_log.error(e)

    async def get(self, *args):
        try:
            result = await self.instance.get(*args)
        except Exception as e:
            app_log.error(e)
        else:
            if result:
                return json.loads(result)

    async def update_cache(self, db_conn):
        """
        Get the price history of each smartphone and cache the results to redis
        :param db_conn: connection to postgres db
        :return: None
        """
        smartphones = tables.Smartphones.__table__
        phones = await db_conn.fetch_all(query=smartphones.select()
                                         .with_only_columns([smartphones.c.phone_id]))

        await self.set('phone_ids', [phone['phone_id'] for phone in phones])

        for phone in jsonable_encoder(phones):
            query = f"""select sub.phone_name,  date_trunc(:timeframe, converted_listings.date_added)as datetime, 
            round(avg(converted_listings.price)::decimal, 1 ) as average from (select * from phonelistings inner join 
            smartphones on smartphones.phone_id=phonelistings.phone_id where smartphones.phone_id = 
            :id ) sub inner join (select  item_id, title, date_added, 
            canadian_price_base as price from listings) as converted_listings on 
            converted_listings.item_id=sub.item_id AND converted_listings.date_added=sub.date_added group by 
            datetime, sub.phone_name order by datetime;"""

            result = await db_conn.fetch_all(query=query, values={"id": phone['phone_id']})
            await self.set(phone['phone_id'], result)

    async def close_redis(self):
        app_log.debug("closing redis connection")
        self.instance.close()
        await self.instance.wait_closed()
        app_log.debug("redis connection closed")
