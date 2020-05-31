import time
import datetime
import calendar

# spider run mode selector
switch = int(input('\nSWITCH SPIDER RUN MODE:\n\t'
                   '- DEMO........(0 + enter)\n\t'
                   '- AUTOMATIC...(1 + enter)\n'))

# input 4 digits
global depart_month, return_month
enter = input('\nINPUT TIME FRAME: \n')

# process data
split = list(enter)
# time frame variables
dep = split[0] + split [1]
ret = split[2] + split [3]
# process goes on
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

# todo: SET GMT CURRENT DAY!
# today = time.localtime()  # fixme CURRENT DAY
# both localtime() and gmtime() returns an struct object, but but there is a time
# difference between them, here we must use gmtime () to get the correct day :)
today = time.gmtime()
t = today.tm_mday

# todo: mandatory to depart/return next month...
if t > start < end:
    depart_month = 2
    return_month = 2
    print("next month departure & return!")

# todo: impossible!
elif t > start > end:
    print("wrong date, the day of departure cannot be less than ", t)

# todo: mandatory to depart/return using both months...
elif t < start > end:
    depart_month = 1
    return_month = 2
    print("current month departure & next month return!")

# todo: possible either of months _REQUIRES CHOICE!
elif t < start < end:
    answer = input("Are you going to travel next month? (y/n)")
    if answer != 'y':
        depart_month = 1
        return_month = 1
        print("current month departure!")
    else:
        depart_month = 2
        return_month = 2
        print("next month departure!")

print('\nACTIVATING SPIDER!\n')  # todo No. WEEK MONTH & WEEK DAY

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


def week(year, month, day):
    first_week_month = datetime.datetime(year, month, 1).isocalendar()[1]
    if month == 1 and first_week_month > 10:
        first_week_month = 0
    user_date = datetime.datetime(year, month, day).isocalendar()[1]
    if month == 1 and user_date > 10:
        user_date = 0
    return user_date - first_week_month + 1


depart_month = str(depart_month)
dep_w = week(2020, m1, d1)
depart_week = str(dep_w + 1)
dep_d = datetime.datetime(2020, m1, d1).weekday()
depart_day = str(dep_d + 1)

return_month = str(return_month)
ret_w = week(2020, m2, d2)
return_week = str(ret_w + 1)
ret_d = datetime.datetime(2020, m2, d2).weekday()
return_day = str(ret_d + 1)

# cryptography
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZA'
number = '01234567890'
def code_builder(chunk):
    global skip
    split = list(chunk)
    char1 = split[0]
    char2 = split[1]
    char3 = split[2]
    char4 = split[3]
    skip = True
    i = 0
    while skip:
        if alpha[i] == char1:
            char1 = alpha[i + 1]
            skip = False
        else:
            skip += 1
        i += 1
    skip = True
    i = 0
    while skip:
        if alpha[i] == char2:
            char2 = alpha[i + 1]
            skip = False
        else:
            skip += 1
        i += 1
    skip = True
    i = 0
    while skip:
        if number[i] == char3:
            char3 = number[i + 1]
            skip = False
        else:
            skip += 1
        i += 1
    skip = True
    i = 0
    while skip:
        if number[i] == char4:
            char4 = number[i + 1]
            skip = False
        else:
            skip += 1
        i += 1

    code = char1 + char2 + char3 + char4
    return code