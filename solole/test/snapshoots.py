import os
import time
import datetime
from datetime import date
import calendar
import numpy as np

global depart_month
global return_month

# todo vademecum:
# time, time(), localtime(), asctime(), ctime(), mktime(), altzone, sleep(), tzset(), strftime()
# datetime, timedelta(),
# datetime.datetime, utcnow()

print('\n\tsnap!\n')
my_date = date.today()

d = datetime.datetime.today().weekday()
print("today's weekday: ", d)

d = calendar.day_name[my_date.weekday()]
print(d)

print("\n\tsnap:\n")
t = time.localtime()
print("time.asctime(t): %s " % time.asctime(t))

print("\n\tsnap:\n")
localtime = time.asctime(time.localtime(time.time()))
print("Current local time:", localtime)

print("\n\tsnap:\n")
print("time.ctime() : %s" % time.ctime())

print("\n\tsnap:\n")  # todo: WAIT
print("Start: %s wait 2 seconds please ..." % time.ctime())
time.sleep(2)
print("Stop: %s" % time.ctime())

print("\n\tsnap:\n")
now = datetime.datetime.utcnow()
print("now: ", now)

print("\n\tsnap:\n")
now = datetime.datetime.utcnow()
an_hour_ago = now - datetime.timedelta(hours=1)
print("an hour ago: ", an_hour_ago)

print("\n\tsnap:\n")
now = datetime.datetime.utcnow()
yesterday = now - datetime.timedelta(days=1)
print("yesterday: ", yesterday)

print("\n\tsnap:\n")  # todo: CALCULATE
today = datetime.datetime.utcnow()
days = 6
print("check in:  ", today)
check_out = today + datetime.timedelta(days - 1)
print("check out: ", check_out)

print("\n\tsnap:\n")
week = datetime.timedelta(weeks=1)
print("a week are: ", week)

print("\n\tsnap:\n")
ticks = time.time()
print("Tick number from 12:00 am, January 1, 1970:", ticks)

print("\n\tsnap:\n")  # todo: CALENDAR
cal = calendar.month(2020, 5)
print("Here is the calendar: ", cal)  # CALENDAR #

print("\n\tsnap:\n")
t = (2018, 3, 28, 17, 3, 38, 1, 48, 0)
secs = time.mktime(t)
print("time.mktime(t) : %f" % secs)
print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs)))

print("\n\tsnap:\n")
print("time.altzone %d " % time.altzone)

print("\n\tsnap:\n")
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()
print(time.strftime('%X %x %Z'))

print("\n\tsnap:\n")
os.environ['TZ'] = 'AEST-10AEDT-11,M10.5.0,M3.5.0'
time.tzset()
print(time.strftime('%X %x %Z'))

print("\n\tsnap:\n")
#  f"http://www.phenomena-experience.com/programacion-mensual/{self.current_date}.html"
current_date = datetime.datetime.now().strftime("%m-%Y")
print("current date: ", current_date)

print("\n\tsnap:\n")
print("snapshoot1 ", datetime.datetime.now().year)
print("snapshoot2 ", time.strftime("%d/%m/%Y"))
print("snapshoot3 ", time.strftime("%d/%m/%Y/%h"))
print("snapshoot4 ", datetime.datetime.today().strftime("%A %d de %B de %Y"))

print("\n\tsnap:\n")  # todo: STRUCT
localtime = time.localtime(time.time())
print("localtim STRUCT object: ", localtime)
gtmtime = time.gmtime(time.time())
print("gmtime STRUCT object: ", gtmtime)

print("\n\tSNAP!:\n")  # Todo No. MONTH -> input time_frame calendar search engine management:

# input 4 digits
enter = input('Input time frame: \n')

# process data
split = list(enter)
check_type = split[0]
check = int(check_type)
if check == 0:
    check_in = split[1]
else:
    check_in = split[0] + split[1]
check_type = split[2]
check = int(check_type)
if check == 0:
    check_out = split[3]
else:
    check_out = split[2] + split[3]

# print data
print("check in: ", check_in, " - check out: ", check_out)

# cast data
start = int(check_in)
end = int(check_out)

# verify cast
print("cast validation ->\tstart - end: ", start - end)

# todo: SET GMT CURRENT DAY!
# today = time.localtime()  # fixme CURRENT DAY
# both localtime() and gmtime() returns an struct object, but but there is a time
# difference between them, here we must use gmtime () to get the correct day :)
today = time.gmtime()
t = today.tm_mday
print("GMT CURRENT DAY: ", t)

# todo: mandatory to depart/return next month...
if t > start < end:
    depart_month = 2
    return_month = 2
    print("next month departure & return!")
    print("\nhappy holidays!\n")

# todo: impossible!
elif t > start > end:
    print("wrong date, the day of departure cannot be less than ", t)

# todo: mandatory to depart/return using both months...
elif t < start > end:
    depart_month = 1
    return_month = 2
    print("current month departure & next month return!")
    print("\nhappy holidays!\n")

# todo: possible either of months _REQUIRES CHOICE!
elif t < start < end:
    answer = input("Are you going to travel next month? (y/n)")
    if answer != 'y':
        depart_month = 1
        return_month = 1
        print("current month departure!")
        print("\nhappy holidays!\n")
    else:
        depart_month = 2
        return_month = 2
        print("next month departure!")
        print("\nhappy holidays!\n")

print('\n\tSNAP!\n')  # todo No. WEEK MONTH & WEEK DAY

# no week month function


# fixme: pattern REF:
#  https://stackoverflow.com/questions/3806473/python-week-number-of-the-month
#  calendar.setfirstweekday(6)
#  def get_week_of_month(year, month, day):
#      x = np.array(calendar.monthcalendar(year, month))
#      week_of_month = np.where(x == day)[0][0] + 1
#      return week_of_month

# fixme _DEPART:
# set current month number
calendar.setfirstweekday(6)
start_month = datetime.datetime.now().strftime("%m")
# zero out left
start_month = start_month.lstrip('+-0')
# cast int type
start_month = int(start_month)
# switch nex month in case
if depart_month != 1:
    start_month = start_month + 1
# set current month
m1 = start_month
# set start day
d1 = start

# fixme _RETURN:
# set current month number
calendar.setfirstweekday(6)
end_month = datetime.datetime.now().strftime("%m")
# zero out left
end_month = end_month.lstrip('+-0')
# cast int type
end_month = int(end_month)
# switch nex month in case
if return_month != 1:
    end_month = end_month + 1
# set current month
m2 = end_month
# set start day
d2 = end


# it's OK!
def week(year, month, day):
    first_week_month = datetime.datetime(year, month, 1).isocalendar()[1]
    if month == 1 and first_week_month > 10:
        first_week_month = 0
    user_date = datetime.datetime(year, month, day).isocalendar()[1]
    if month == 1 and user_date > 10:
        user_date = 0
    return user_date - first_week_month + 1


print("No depart month: ", depart_month)
print("No depart week: ", week(2020, m1, d1))
depart_day = datetime.datetime(2020, m1, d1).weekday()
print("No depart day: ", depart_day + 1)


print("\nNo return month: ", return_month)
print("No return week: ", week(2020, m2, d2))
return_day = datetime.datetime(2020, m2, d2).weekday()
print("No return day: ", return_day + 1)

