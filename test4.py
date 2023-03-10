import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def generate_time(times):
    today = date.today()
    for day in range(12):
        times.append({"start_time": today-timedelta(days=day+1), "end_time": today-timedelta(days=day)})
    for week in range(12):
        times.append({"start_time": today-timedelta(weeks=week+1), "end_time": today-timedelta(weeks=week)})
    for month in range(12):
        times.append({"start_time": today-relativedelta(months=month+1), "end_time": today-relativedelta(months=month)})
    return times

#
# for time in generate_time([]):
#     print(time)

today = date.today()
print(str(today).replace('-', ''))
