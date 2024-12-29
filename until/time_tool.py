import datetime
import time

def time_change(time_str, value):
    print(time_str)
    fd = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    eta = (fd + datetime.timedelta(hours=value)).strftime("%Y-%m-%d")
    return eta

def time_format(time_string="", time_string_condition="", is_need_hms=False, time_format="", hours=0):
    """
    time_string
    time_string_condition
    is_need_hms
    time_format
    hours
    """
    if time_format:
        if "Z" in time_format:
            time_format = time_format.replace('Z', "")
            time_format = time_format.split(".")[0]
            datenumber = time_format.split("T")[0] + " " + time_format.split("T")[1]
            print(datenumber,'****')
            datenumber = time_change(datenumber, hours)
            return datenumber
        else:
            if "+" in time_format:
                datenumber = time_format.split("T")[0] + " " + time_format.split("T")[1].split("+")[0]
                datenumber = time_change(datenumber, hours)
                return datenumber
            elif "-" in time_format:
                datenumber = time_format.split("T")[0] + " " + time_format.split("T")[1].split("-")[0]
                datenumber = time_change(datenumber, hours)
                return datenumber



def saveTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def timestamp_to_date_str(timestamp,timeformat:str):
    """
    将时间戳转换为YYYY-MM-DD格式的日期字符串

    参数:
    timestamp (int或float): 以秒为单位的时间戳

    返回:
    str: 格式化后的日期字符串，格式为YYYY-MM-DD
    """
    date_obj = datetime.datetime.fromtimestamp(timestamp)
    return date_obj.strftime(timeformat)