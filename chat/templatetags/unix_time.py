from django import template
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

tz = ZoneInfo("Asia/Tashkent")
register = template.Library()

@register.filter
def unix_to_time(ts):
    return datetime.fromtimestamp(int(ts), tz=tz).strftime("%H:%M")

@register.filter
def unix_to_date(ts):
    return datetime.fromtimestamp(int(ts), tz=tz).strftime("%d.%m.%Y")