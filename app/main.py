from fastapi import FastAPI, HTTPException
from app.database.db import database
from app.database.db import tables

app = FastAPI()
smartphones = tables.smartphones


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/phones/")
async def all_phones():
    phones = await database.fetch_all(query=smartphones.select()
                                      .with_only_columns([smartphones.c.phone_id, smartphones.c.phone_name]))
    return phones


@app.get("/phones/{_id}")
async def phone_id(_id: str):
    phone = await database.fetch_one(query=smartphones.select().filter(smartphones.c.phone_id == _id)
                                     .with_only_columns([smartphones.c.phone_id, smartphones.c.phone_name]))
    if not phone:
        raise HTTPException(status_code=404, detail="Item not found")
    return phone
