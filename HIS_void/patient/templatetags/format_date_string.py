from django import template

register = template.Library()


@ register.filter(name = "ymd2md")
def ymd2md(ymd_string:str):
    """
    将形如 '2021-05-15', '2021-5-15', '2021-5-5' 的日期字符串转为形如 '05-15' 的字符串
    """
    return '-'.join(map(lambda x: x.rjust(2, '0'), ymd_string.split('-')[1:]))
