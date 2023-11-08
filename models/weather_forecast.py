import datetime

from pydantic import BaseModel


class WeatherForecast(BaseModel):
    wfc_date: datetime.date
    wfc_temp_c: int
    wfc_temp_f: int


class WeatherForecastIn(BaseModel):
    wfc_date: datetime.date
    wfc_temp_c: int
