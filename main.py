import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from db.forecast_db import ForecastDB
from models.weather_forecast import WeatherForecast, WeatherForecastIn

app = FastAPI()

db = ForecastDB()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/forecasts/", response_model=list[WeatherForecast])
async def get_all():
    return db.get_all()


@app.get("/forecasts/{wfc_date}", response_model=WeatherForecast)
async def get_one(wfc_date: datetime.date):
    query = db.get(wfc_date)
    if query is not None:
        return query

    raise HTTPException(status_code=404, detail='Forecast not found')


@app.get("/forecasts/find/", response_model=list[WeatherForecast])
async def get_one(from_date: datetime.date, to_date: datetime.date):
    query = db.find(from_date, to_date)
    if query is not None:
        return query

    raise HTTPException(status_code=404, detail='No forecast found')


@app.post("/forecasts/add/", response_model=WeatherForecast)
async def add(wfc: WeatherForecastIn):
    query = db.add(wfc)
    if query is not None:
        return query

    raise HTTPException(status_code=500, detail='Forecast with date already exists')


@app.put("/forecasts/update/{wfc_date}", response_model=WeatherForecast)
async def update(wfc_date: datetime.date, new_temp_c: int):
    query = db.update(wfc_date, new_temp_c)
    if query is not None:
        return query

    raise HTTPException(status_code=404, detail='Forecast not found')


@app.delete("/forecasts/{wfc_date}")
async def delete(wfc_date: datetime.date):
    if db.delete(wfc_date):
        return {'message': 'Forecast was deleted successfully'}

    raise HTTPException(status_code=404, detail='Forecast not found')


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
