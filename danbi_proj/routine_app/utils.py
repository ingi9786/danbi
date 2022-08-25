from datetime import date
from rest_framework.response import Response



def convert_day(arg):
    daydic = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    y = int(arg[:4])
    m = int(arg[4:6])
    d = int(arg[6:])
    _date = date(y, m, d)
    _day  = date.weekday(_date)
    return daydic[_day]


def get_today():
    return "".join(str(date.today()).split('-'))


def is_valid_date(arg):
    return True if arg.isdigit() and len(arg)==8 else False


def Response_200(data=None, action=None, res='ROUTINE'):
    msg = {
        "msg"   : f"{action} was successful.",
        "status": f"{res}{action}_OK_200"
        }
    return Response({ "data": data, "message": msg}) if data is not None else Response({"message":msg})


def Response_201(data, action, res="ROUTINE"):
    return Response(
        {
            "data": data,
            "message": {
                "msg"   : f"You have successfully created the {res}.",
                "status": f"{res}{action}_OK_201" 
            }
        })


def Response_404(res='ROUTINE'):
    msg= {
        "msg"    : f"{res} could not be found.",
        "status" : "NOT_FOUND_404"
        }
    return Response({"message":msg})


def Response_400():
    msg = {
        "msg": "Invalid data type.",
        "status": "BAD_REQUEST_400"
        }
    return Response({"message":msg})