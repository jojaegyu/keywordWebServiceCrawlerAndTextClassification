from collections import defaultdict


def operator(curr_time, time):
    year, month, day, hour, minute, second = map(int, curr_time.split(":"))
    pday, phour, pminute, psecond = map(int, time.split(":"))
    day += pday
    hour += phour
    minute += pminute
    second += psecond
    if second >= 60:
        cnt = second // 60
        second -= 60 * cnt
        minute += 1 * cnt
    if minute >= 60:
        cnt = minute // 60
        minute -= 60 * cnt
        hour += 1 * cnt
    if hour >= 24:
        cnt = hour // 24
        hour -= 24 * cnt
        day += 1 * cnt
    if day >= 31:
        cnt = day // 30
        day -= 30
        month += 1
    if month >= 13:
        month -= 12
        year += 1
    return ':'.join(list(map(str, [year, month, day, hour, minute, second])))


def solution(s, times):
    visited = defaultdict(lambda: False)
    days = [s]

    for time in times:
        days.append(operator(days[-1], time))

    for day in days:
        year, month, day, hour, minute, second = day.split(":")
        visited[(year, month, day)] = True

    tmp = days[0].split(":")
    tmp2 = days[-1].split(":")

    start = (tmp[0], tmp[1], tmp[2])
    end = (tmp2[0], tmp2[1], tmp2[2])

    differ = 1
    differ += (int(end[0]) - int(start[0])) * 365
    differ += (int(end[1]) - int(start[1])) * 30
    differ += (int(end[2]) - int(start[2]))
    print(visited)
    print(start, end)
    print(differ)

