import datetime as DateTime
# All credit goes to chatgpt for this one.
# I'm sure it would have been a fun and quick side-project
# but it was a roadblock at 2 in the morning soooooo here
# we are.

def day_suffix(day: int) -> str:
    if 11 <= day <= 13:
        return "th"
    if day % 10 == 1:
        return "st"
    elif day % 10 == 2:
        return "nd"
    elif day % 10 == 3:
        return "rd"
    else:
        return "th"

def beautify_datetime(dt: DateTime.datetime, now: DateTime.datetime) -> str | None:
    if now is None:
        now = DateTime.datetime.now()
    if dt is None:
        return None
    # Get current date for comparison
    today = now.date()
    tomorrow = today + DateTime.timedelta(days = 1)
    current_week_end = today + DateTime.timedelta(days=(6 - today.weekday()))  # Last day of the week (Sunday)
    # Format time
    time_str = dt.strftime("%-I:%M%p").lower()
    if dt.date() < today:
        day = dt.day
        month = dt.strftime("%B")
        year = dt.year
        return f"{month} {day}{day_suffix(day)}, {year}, at {time_str}"
    elif dt.date() == today:
        return f"{time_str}"
    elif dt.date() <= tomorrow:
        return f"Tomorrow at {time_str}"
    elif today < dt.date() <= current_week_end:
        day_of_week = dt.strftime("%A")
        return f"{day_of_week} at {time_str}"
    elif dt.year == now.year:
        day = dt.day
        month = dt.strftime("%B")
        return f"{month} {day}{day_suffix(day)} at {time_str}"
    else:
        day = dt.day
        month = dt.strftime("%B")
        year = dt.year
        return f"{month} {day}{day_suffix(day)}, {year}, at {time_str}"
