from pydblite import Base


def get_cursor(db_name):
    if db_name == 'weather_data':
        db = Base('storage/weather_data.pdl')
        if not db.exists():
            db.create(
                'low',
                'tmw',
                'high',
                'temp',
                'date',
                'text',
                'code',
                'history',
                'uniq_id',
                'location',
                'astronomy',
                'atmosphere',
                'country_name',
                'created_date',
                'location_name'
            )
    elif db_name == 'locations':
        db = Base('storage/locations.pdl')
        if not db.exists():
            db.create(
                'uniq_id',
                'location',
                'created_date'
            )
    else:
        raise Exception('Please Enter Valid Name!')

    cursor = db.open()
    return cursor

