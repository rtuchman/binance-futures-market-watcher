from datetime import datetime, timedelta

def get_next_funding_time() -> datetime:
    """
    Returns the next funding time as a `datetime` object.
    
    The next funding time is determined based on the current time and a set of conditions.
    
    :return: The next funding time as a `datetime` object.
    """
    now = datetime.utcnow()
    if now.hour < 8:
        next_hour = 8
    elif now.hour < 16:
        next_hour = 16
    else:
        next_hour = 0
        now += timedelta(days=1)  # move to the next day if current time is past 16:00

    next_funding_time = datetime(now.year, now.month, now.day, next_hour)
    return next_funding_time

def format_timedelta(td: timedelta) -> str:
    """
    Formats a timedelta object as a string representing the duration in hours, minutes, and seconds.

    Args:
        td (timedelta): The duration to be formatted.

    Returns:
        str: The duration formatted as "HH:MM:SS".
    """
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"