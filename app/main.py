import asyncpg.exceptions
from fastapi import FastAPI, HTTPException
from typing import Union
from sqlalchemy import func

from app.database.db import database
from app.database.db import tables

app = FastAPI()
smartphones = tables.Smartphones.__table__


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/phones/")
async def all_phones(detailed: Union[bool, None] = None):
    if detailed:
        phones = await database.fetch_all(query=smartphones.select())
    else:
        phones = await database.fetch_all(query=smartphones.select()
                                          .with_only_columns([smartphones.c.phone_id, smartphones.c.phone_name]))
    return phones


@app.get("/phones/brands")
async def phone_brands():
    phones = await database.fetch_all(query=smartphones.select()
                                      .with_only_columns([smartphones.c.brand]).distinct())
    return phones


@app.get("/phones/series")
async def phone_series(brand: str):
    phones = await database.fetch_all(query=smartphones.select().filter(func.lower(smartphones.c.brand) == brand.lower())
                                      .with_only_columns([smartphones.c.series]).distinct())
    return phones


@app.get("/phones/models")
async def phone_models(brand: str, series: str):
    phones = await database.fetch_all(
        query=smartphones.select().filter(func.lower(smartphones.c.brand) == brand.lower())
        .filter(func.lower(smartphones.c.series) == series.lower())
        .with_only_columns([smartphones.c.name]).distinct())
    return phones


@app.get("/phones/{_id}")
async def phone_id(_id: str, detailed: Union[bool, None] = None):
    if detailed:
        phone = await database.fetch_one(query=smartphones.select().filter(smartphones.c.phone_id == _id))
    else:
        phone = await database.fetch_one(query=smartphones.select().filter(smartphones.c.phone_id == _id)
                                         .with_only_columns([smartphones.c.phone_id, smartphones.c.phone_name]))
    if not phone:
        raise HTTPException(status_code=404, detail="Item not found")
    return phone


@app.get("/phones/{_id}/price_history")
async def price_history(_id: str, timeframe: str = "year"):
    query = f"""select sub.phone_name,  date_trunc(:timeframe, converted_listings.date_added)as datetime, count(converted_listings) as sample_size,
	        round(avg(converted_listings.price)::decimal, 1 ) as average, round(min(converted_listings.price)::decimal, 1 ) as cheapest, 
	round(max(converted_listings.price)::decimal, 1 ) as costliest
	from
		(select *
		from phonelistings
		inner join smartphones on smartphones.phone_id=phonelistings.phone_id
	 	where smartphones.phone_id = :id
		) sub
	inner join (select  item_id, title, date_added,
		case
		when currency = 'USD' then price * 1.28
		when currency = 'EUR' then price * 1.36
		when currency = 'AUD' then price * 0.91
		when currency = 'GBP' then price * 1.61
		when currency = 'CAD' then price
		end as price 
		from listings) as converted_listings
		on converted_listings.item_id=sub.item_id
		AND converted_listings.date_added=sub.date_added
	group by datetime, sub.phone_name
	order by datetime
    ;"""
    try:
        result = await database.fetch_all(query=query, values={"timeframe": timeframe, "id": _id})
    except asyncpg.exceptions.InvalidParameterValueError:
        error_message = f"timestamp '{timeframe}' is not a valid parameter"
        raise HTTPException(status_code=400, detail=error_message)
    else:
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
    return result
