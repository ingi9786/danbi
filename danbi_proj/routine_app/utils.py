from datetime import date

# Convert 날짜(str) to 요일(str)
def convert_day(arg):
    daydic = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    y = int(arg[:4])
    m = int(arg[4:6])
    d = int(arg[6:])
    _date = date(y, m, d)
    _day  = date.weekday(_date)
    return daydic[_day]

# 오늘날짜를 반환하는 함수
def get_today():
    return "".join(str(date.today()).split('-'))

# date param이 유효한지 확인
def is_valid_date(arg):
    return True if arg.isdigit() and len(arg)==8 else False

             