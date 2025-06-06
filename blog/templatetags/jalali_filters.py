import jdatetime
from django import template

mounts = [
    "",
    "Farvardin",
    "Ordibehesht",
    "Khordad",
    "Tir",
    "Mordad",
    "Shahrivar",
    "Mehr",
    "Aban",
    "Azar",
    "Dey",
    "Bahman",
    "Esfand",
]

register = template.Library()


@register.filter
def to_jalali(value):
    if not value:
        return ""
    jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
    date = jalali_date.strftime("%d %B %Y").split()
    print(mounts.index(date[1]))
    return date[0] + " / " + str(mounts.index(date[1])) + " / " + date[2]


@register.filter
def times(number):
    return range(number)


@register.filter
def to_str(number):
    return str(number)


@register.filter
def final_price(quantity, price):
    return str(int(quantity) * int(price))
