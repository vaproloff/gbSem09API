import datetime

from models.weather_forecast import WeatherForecastIn, WeatherForecast


class ForecastDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__forecasts: list[WeatherForecast] = []

    def get_all(self) -> list[WeatherForecast]:
        return self.__forecasts

    def get(self, wfc_date: datetime.date) -> WeatherForecast | None:
        for fc in self.__forecasts:
            if fc.wfc_date == wfc_date:
                return fc
        return None

    def find(self, from_date: datetime.date, to_date: datetime.date) -> list[WeatherForecast] | None:
        forecasts_found = []
        for fc in self.__forecasts:
            if from_date <= fc.wfc_date <= to_date:
                forecasts_found.append(fc)
        return forecasts_found if len(forecasts_found) else None

    def add(self, forecast: WeatherForecastIn) -> WeatherForecast | None:
        for fc in self.__forecasts:
            if fc.wfc_date == forecast.wfc_date:
                return None

        new_forecast = WeatherForecast(wfc_date=forecast.wfc_date,
                                       wfc_temp_c=forecast.wfc_temp_c,
                                       wfc_temp_f=32 + int(forecast.wfc_temp_c / 0.5556))
        self.__forecasts.append(new_forecast)
        return new_forecast

    def update(self, wfc_date: datetime.date, new_temp: int) -> WeatherForecast | None:
        for fc in self.__forecasts:
            if fc.wfc_date == wfc_date:
                fc.wfc_temp_c = new_temp
                fc.wfc_temp_f = 32 + int(new_temp / 0.5556)
                return fc
        return None

    def delete(self, wfc_date: datetime.date) -> bool:
        for fc in self.__forecasts:
            if fc.wfc_date == wfc_date:
                self.__forecasts.remove(fc)
                return True
        return False
