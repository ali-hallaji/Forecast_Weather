import time
import uuid
import datetime

from weather import Unit
from weather import Weather

from config import weather_unit
from db_handler import get_cursor


def get_data_weather_location(city_name):
    weather = Weather(unit=weather_unit)
    location = weather.lookup_by_location(city_name)
    return location

def update_location(name):
    cursor = get_cursor('locations')
    exist = cursor(location=name)
    if not exist:
        cursor.insert(
            uniq_id=str(uuid.uuid1()),
            location=name,
            created_date=datetime.datetime.now()
        )
    else:
        cursor.update(
            exist[0],
            location=name,
        )
    cursor.commit()

def insert_data(name):
    cursor = get_cursor('weather_data')
    case = get_data_weather_location(name)
    if not case:
        return 'Invalid Name!'
    today_f = case.forecast[0]
    tmw_f = case.forecast[1]

    exist = cursor(location_name=name)
    update_location(case.location.city)
    now = datetime.datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    if not exist:
        cursor.insert(
            low=today_f.low,
            tmw=tmw_f,
            high=today_f.high,
            date=now.date(),
            text=case.condition.text,
            temp=case.condition.temp,
            code=case.condition.code,
            history=[(int(case.condition.temp), str_now)],
            uniq_id=str(uuid.uuid1()),
            location=case.location,
            astronomy=case.astronomy,
            atmosphere=case.atmosphere,
            country_name=case.location.country,
            created_date=now,
            location_name=case.location.city,
        )
    else:
        exist[0]['history'].append((int(case.condition.temp), str_now))
        cursor.update(
            exist[0],
            low=today_f.low,
            tmw=tmw_f,
            high=today_f.high,
            text=case.condition.text,
            temp=case.condition.temp,
            history=exist[0]['history'],
            location=case.location,
            astronomy=case.astronomy,
            atmosphere=case.atmosphere,
        )
    cursor.commit()

def update_data():
    cursor = get_cursor('weather_data')
    for location in get_cursor('locations'):
        time.sleep(0.2)
        case = get_data_weather_location(location['location'])
        today_f = case.forecast[0]
        tmw_f = case.forecast[1]

        exist = cursor(location_name=location['location'])
        now = datetime.datetime.now()
        str_now = now.strftime('%Y-%m-%d %H:%M:%S')
        if not exist:
            cursor.insert(
                low=today_f.low,
                tmw=tmw_f,
                high=today_f.high,
                date=now.date(),
                text=case.condition.text,
                temp=case.condition.temp,
                code=case.condition.code,
                history=[(case.condition.temp, str_now)],
                uniq_id=str(uuid.uuid1()),
                location=case.location,
                astronomy=case.astronomy,
                atmosphere=case.atmosphere,
                country_name=case.location.country,
                created_date=now,
                location_name=case.location.city,
            )
        else:
            exist[0]['history'].append((int(case.condition.temp), str_now))
            cursor.update(
                exist[0],
                low=today_f.low,
                tmw=tmw_f,
                high=today_f.high,
                text=case.condition.text,
                temp=case.condition.temp,
                history=exist[0]['history'],
                location=case.location,
                astronomy=case.astronomy,
                atmosphere=case.atmosphere,
            )
        cursor.commit()
