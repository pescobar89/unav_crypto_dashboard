import datetime as dt
import time
import re


class DateFormatter:

    def __init__(self):
        pass

    @staticmethod
    def date_formats(date):
        # Comprobamos el formato de la fecha string de entrada
        #         pattern = re.compile(r'\d{4}\-[0-1]\d\-[0-3]\d\s[0-2]\d\:[0-5]\d\:[0-5]\d') # Mejorable, quizas mejor hacerlo en la conversion a datetime
        date_string = date
        date_list = re.split('-| |:', date)
        date_datetime = dt.datetime(*[int(x) for x in date_list], tzinfo=dt.timezone.utc)  # Mirar meter un try/except
        date_unix = int(time.mktime(date_datetime.timetuple()))
        formats = {'string': date_string, 'list': date_list, 'datetime': date_datetime, 'unix': date_unix}
        return(formats)
