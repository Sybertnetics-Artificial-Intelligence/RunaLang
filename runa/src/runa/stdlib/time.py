"""
Runa Standard Library - Time Module

Provides time and date operations for Runa programs.
"""

import time as py_time
import datetime as py_datetime
from datetime import timezone

def current_timestamp():
    """Get the current Unix timestamp."""
    return py_time.time()

def current_date():
    """Get the current date as a string."""
    return py_datetime.date.today().isoformat()

def current_time():
    """Get the current time as a string."""
    return py_datetime.datetime.now().time().isoformat()

def current_datetime():
    """Get the current date and time as a string."""
    return py_datetime.datetime.now().isoformat()

def current_utc_datetime():
    """Get the current UTC date and time as a string."""
    return py_datetime.datetime.now(timezone.utc).isoformat()

def format_datetime(dt, format_string):
    """Format a datetime object using a format string."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.strftime(format_string)

def parse_datetime(date_string, format_string=None):
    """Parse a date string into a datetime object."""
    if format_string:
        return py_datetime.datetime.strptime(date_string, format_string)
    else:
        # Try to parse ISO format
        try:
            return py_datetime.datetime.fromisoformat(date_string)
        except ValueError:
            raise Exception(f"Could not parse datetime string: {date_string}")

def sleep_for_seconds(seconds):
    """Pause execution for a specified number of seconds."""
    py_time.sleep(seconds)

def sleep_for_milliseconds(milliseconds):
    """Pause execution for a specified number of milliseconds."""
    py_time.sleep(milliseconds / 1000.0)

def timestamp_to_datetime(timestamp):
    """Convert a Unix timestamp to a datetime string."""
    return py_datetime.datetime.fromtimestamp(timestamp).isoformat()

def datetime_to_timestamp(dt):
    """Convert a datetime to a Unix timestamp."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.timestamp()

def add_seconds_to_datetime(dt, seconds):
    """Add seconds to a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt + py_datetime.timedelta(seconds=seconds)
    return result.isoformat()

def add_minutes_to_datetime(dt, minutes):
    """Add minutes to a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt + py_datetime.timedelta(minutes=minutes)
    return result.isoformat()

def add_hours_to_datetime(dt, hours):
    """Add hours to a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt + py_datetime.timedelta(hours=hours)
    return result.isoformat()

def add_days_to_datetime(dt, days):
    """Add days to a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt + py_datetime.timedelta(days=days)
    return result.isoformat()

def subtract_seconds_from_datetime(dt, seconds):
    """Subtract seconds from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt - py_datetime.timedelta(seconds=seconds)
    return result.isoformat()

def subtract_minutes_from_datetime(dt, minutes):
    """Subtract minutes from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt - py_datetime.timedelta(minutes=minutes)
    return result.isoformat()

def subtract_hours_from_datetime(dt, hours):
    """Subtract hours from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt - py_datetime.timedelta(hours=hours)
    return result.isoformat()

def subtract_days_from_datetime(dt, days):
    """Subtract days from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    result = dt - py_datetime.timedelta(days=days)
    return result.isoformat()

def calculate_time_difference(dt1, dt2):
    """Calculate the difference between two datetimes in seconds."""
    if isinstance(dt1, str):
        dt1 = py_datetime.datetime.fromisoformat(dt1)
    if isinstance(dt2, str):
        dt2 = py_datetime.datetime.fromisoformat(dt2)
    
    diff = dt2 - dt1
    return diff.total_seconds()

def get_day_of_week(dt):
    """Get the day of the week for a datetime (0=Monday, 6=Sunday)."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.weekday()

def get_day_name(dt):
    """Get the name of the day for a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.strftime('%A')

def get_month_name(dt):
    """Get the name of the month for a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.strftime('%B')

def get_year(dt):
    """Get the year from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.year

def get_month(dt):
    """Get the month from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.month

def get_day(dt):
    """Get the day from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.day

def get_hour(dt):
    """Get the hour from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.hour

def get_minute(dt):
    """Get the minute from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.minute

def get_second(dt):
    """Get the second from a datetime."""
    if isinstance(dt, str):
        dt = py_datetime.datetime.fromisoformat(dt)
    return dt.second

def create_datetime(year, month, day, hour=0, minute=0, second=0):
    """Create a datetime from components."""
    dt = py_datetime.datetime(year, month, day, hour, minute, second)
    return dt.isoformat()

def is_leap_year(year):
    """Check if a year is a leap year."""
    return py_datetime.date(year, 1, 1).year % 4 == 0 and (py_datetime.date(year, 1, 1).year % 100 != 0 or py_datetime.date(year, 1, 1).year % 400 == 0)

def days_in_month(year, month):
    """Get the number of days in a month."""
    if month == 12:
        next_month = py_datetime.date(year + 1, 1, 1)
    else:
        next_month = py_datetime.date(year, month + 1, 1)
    
    this_month = py_datetime.date(year, month, 1)
    return (next_month - this_month).days

def measure_execution_time(func, *args, **kwargs):
    """Measure the execution time of a function."""
    start_time = py_time.time()
    result = func(*args, **kwargs)
    end_time = py_time.time()
    return {
        'result': result,
        'execution_time': end_time - start_time
    }

# Runa-style function names for natural language calling
get_current_timestamp = current_timestamp
get_current_date = current_date
get_current_time = current_time
get_current_datetime = current_datetime
get_current_utc_time = current_utc_datetime
format_date_time = format_datetime
parse_date_time = parse_datetime
wait_for_seconds = sleep_for_seconds
wait_for_milliseconds = sleep_for_milliseconds
convert_timestamp_to_datetime = timestamp_to_datetime
convert_datetime_to_timestamp = datetime_to_timestamp
add_time_to_datetime = add_seconds_to_datetime
subtract_time_from_datetime = subtract_seconds_from_datetime
find_time_difference = calculate_time_difference
get_weekday = get_day_of_week
get_name_of_day = get_day_name
get_name_of_month = get_month_name
extract_year = get_year
extract_month = get_month
extract_day = get_day
extract_hour = get_hour
extract_minute = get_minute
extract_second = get_second
make_datetime = create_datetime
check_if_leap_year = is_leap_year
count_days_in_month = days_in_month
time_function_execution = measure_execution_time