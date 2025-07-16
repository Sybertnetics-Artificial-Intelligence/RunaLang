# Time Module

The Time module provides comprehensive utilities for working with time, dates, timestamps, and timezone operations in Runa programs.

## Overview

The Time module offers a complete set of time manipulation functions with natural language syntax for basic operations and helper functions for advanced use cases.

## Basic Time Operations

### Current Time and Sleep

```runa
Note: Basic time operations use natural language syntax
:End Note

Let current_time be now
Call sleep with seconds as 1.5

Let timestamp be current timestamp
Call print with message as "Current time: " plus current_time
Call print with message as "Timestamp: " plus timestamp
```

### Time Formatting and Parsing

```runa
Let formatted_date be format time as current_time with format as "%Y-%m-%d"
Let formatted_time be format time as current_time with format as "%H:%M:%S"

Let parsed_date be parse time from "2023-12-25" with format as "%Y-%m-%d"
Let parsed_datetime be parse time from "2023-12-25 14:30:00" with format as "%Y-%m-%d %H:%M:%S"

Call print with message as "Formatted date: " plus formatted_date
Call print with message as "Parsed date: " plus parsed_date
```

## Time Arithmetic

### Adding Time

```runa
Let future_time be add 5 days to current_time
Let next_hour be add 1 hour to current_time
Let next_week be add 1 week to current_time
Let next_month be add 1 month to current_time
Let next_year be add 1 year to current_time

Call print with message as "Future time: " plus future_time
Call print with message as "Next hour: " plus next_hour
```

### Subtracting Time

```runa
Let past_time be subtract 3 days from current_time
Let previous_hour be subtract 2 hours from current_time
Let last_week be subtract 1 week from current_time

Call print with message as "Past time: " plus past_time
Call print with message as "Previous hour: " plus previous_hour
```

### Time Differences

```runa
Let start_time be "2023-01-01 10:00:00"
Let end_time be "2023-01-01 15:30:00"

Let diff_seconds be difference in seconds between start_time and end_time
Let diff_minutes be difference in minutes between start_time and end_time
Let diff_hours be difference in hours between start_time and end_time
Let diff_days be difference in days between start_time and end_time

Call print with message as "Difference in hours: " plus diff_hours
```

## Time Comparisons

### Comparing Dates and Times

```runa
Let date1 be "2023-01-01"
Let date2 be "2023-01-15"
Let date3 be "2023-01-10"

Assert is date1 before date2 is equal to true
Assert is date2 after date1 is equal to true
Assert is date1 equal to date1 is equal to true
Assert is date3 between date1 and date2 is equal to true
```

## Date Components

### Extracting Date Parts

```runa
Let dt be "2023-12-25 14:30:45"

Let year be year of dt
Let month be month of dt
Let day be day of dt
Let hour be hour of dt
Let minute be minute of dt
Let second be second of dt

Let weekday be weekday of dt
Let weekday_name be weekday name of dt
Let month_name be month name of dt

Call print with message as "Year: " plus year
Call print with message as "Month: " plus month_name
Call print with message as "Weekday: " plus weekday_name
```

### Date Type Checks

```runa
Let weekend_date be "2023-12-23"  Note: Saturday
Let weekday_date be "2023-12-25"  Note: Monday

Assert is weekend weekend_date is equal to true
Assert is weekday weekday_date is equal to true
```

## Calendar Operations

### Leap Years and Days

```runa
Assert is leap year 2024 is equal to true
Assert is leap year 2023 is equal to false

Let days_in_feb_2024 be days in month of 2024 and 2
Let days_in_feb_2023 be days in month of 2023 and 2

Assert days_in_feb_2024 is equal to 29
Assert days_in_feb_2023 is equal to 28

Let days_in_2024 be days in year 2024
Assert days_in_2024 is equal to 366
```

### Week and Quarter Operations

```runa
Let dt be "2023-06-15"
Let week_num be week of year of dt
Let quarter be quarter of year of dt

Call print with message as "Week: " plus week_num
Call print with message as "Quarter: " plus quarter
```

## Time Boundaries

### Start and End of Periods

```runa
Let dt be "2023-12-25 14:30:45"

Let day_start be start of day of dt
Let day_end be end of day of dt

Let week_start be start of week of dt
Let week_end be end of week of dt

Let month_start be start of month of dt
Let month_end be end of month of dt

Let year_start be start of year of dt
Let year_end be end of year of dt

Call print with message as "Day start: " plus day_start
Call print with message as "Week start: " plus week_start
```

## Age Calculations

### Age and Adult Status

```runa
Let birth_date be "1990-05-15"
Let age be age from birth_date
Let is_adult be is adult with birth_date as birth_date and age_limit as 18

Call print with message as "Age: " plus age
Call print with message as "Is adult: " plus is_adult
```

## Business Day Operations

### Business Day Calculations

```runa
Let start_date be "2023-12-20"  Note: Wednesday
Let end_date be "2023-12-27"    Note: Wednesday

Let business_days be business days between start_date and end_date
Let next_business be next business day after start_date
Let prev_business be previous business day before end_date

Let future_business be add 5 business days to start_date
Let past_business be subtract 3 business days from end_date

Assert is business day start_date is equal to true
Assert is business day "2023-12-23" is equal to false  Note: Saturday
```

## Timezone Operations

### Timezone Conversions

```runa
Let local_tz be local timezone
Let utc_time be current utc time

Let converted_time be convert timezone of "2023-12-25 14:30:00" from "UTC" to "America/New_York"
Let to_utc be convert to utc "2023-12-25 14:30:00" in "America/New_York"
Let from_utc be convert from utc "2023-12-25 19:30:00" to "America/New_York"

Call print with message as "Local timezone: " plus local_tz
Call print with message as "UTC time: " plus utc_time
```

## Relative Time Formatting

### Human-Readable Time

```runa
Let past_time be subtract 2 hours from current_time
Let future_time be add 3 days to current_time

Let relative_past be relative time of past_time
Let relative_future be relative time of future_time

Call print with message as "Past: " plus relative_past  Note: "2 hours ago"
Call print with message as "Future: " plus relative_future  Note: "in 3 days"
```

## Duration Operations

### Duration Formatting and Parsing

```runa
Let duration_seconds be 3661  Note: 1 hour, 1 minute, 1 second
Let formatted_duration be format duration of duration_seconds

Let parsed_seconds be parse duration from "1h 30m 45s"

Call print with message as "Formatted: " plus formatted_duration
Call print with message as "Parsed seconds: " plus parsed_seconds
```

## Date Validation

### Validating Date Strings

```runa
Assert is valid date "2023-12-25" is equal to true
Assert is valid date "2023-13-01" is equal to false  Note: Invalid month

Assert is valid time "14:30:45" is equal to true
Assert is valid time "25:00:00" is equal to false  Note: Invalid hour

Assert is valid datetime "2023-12-25 14:30:45" is equal to true
Assert is valid datetime "2023-12-25 25:30:45" is equal to false
```

## Time Utilities

### Min/Max and Sorting

```runa
Let dt1 be "2023-01-01"
Let dt2 be "2023-12-25"

Let min_dt be minimum datetime of dt1 and dt2
Let max_dt be maximum datetime of dt1 and dt2

Let datetime_list be [dt2, dt1, "2023-06-15"]
Let sorted_list be sort datetimes datetime_list
Let unique_list be unique datetimes datetime_list

Assert min_dt is equal to dt1
Assert max_dt is equal to dt2
```

### Time Ranges

```runa
Let start be "2023-01-01"
Let end be "2023-01-05"
Let step be "1 day"

Let range_list be datetime range from start to end with step as step
Note: Returns ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"]
:End Note
```

## Helper Functions

### Advanced Usage

```runa
Note: For advanced/AI-generated code, use helper functions
:End Note

Let formatted be format with dt as current_time and fmt as "%Y-%m-%d %H:%M:%S"
Let parsed be parse with s as "2023-12-25" and fmt as "%Y-%m-%d"
```

## Error Handling

### Robust Time Operations

```runa
Try:
    Let parsed be parse time from "invalid-date" with format as "%Y-%m-%d"
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Call print with message as "Invalid date format: " plus e
```

## Performance Considerations

### Efficient Time Operations

```runa
Note: For repeated time operations, cache current time
:End Note

Let start_time be now
Note: Perform operations
:End Note
Let end_time be now
Let elapsed be difference in seconds between start_time and end_time
```

## API Reference

### Core Functions

- `now() -> String`: Get current datetime
- `sleep(seconds: Number) -> None`: Pause execution
- `format(dt: String, fmt: String) -> String`: Format datetime
- `parse(s: String, fmt: String) -> String`: Parse datetime
- `timestamp() -> Number`: Get current timestamp

### Time Arithmetic

- `add_seconds(dt: String, seconds: Number) -> String`: Add seconds
- `add_minutes(dt: String, minutes: Number) -> String`: Add minutes
- `add_hours(dt: String, hours: Number) -> String`: Add hours
- `add_days(dt: String, days: Number) -> String`: Add days
- `add_weeks(dt: String, weeks: Number) -> String`: Add weeks
- `add_months(dt: String, months: Number) -> String`: Add months
- `add_years(dt: String, years: Number) -> String`: Add years

### Time Comparisons

- `is_before(dt1: String, dt2: String) -> Boolean`: Check if before
- `is_after(dt1: String, dt2: String) -> Boolean`: Check if after
- `is_equal(dt1: String, dt2: String) -> Boolean`: Check if equal
- `is_between(dt: String, start: String, end: String) -> Boolean`: Check if between

### Date Components

- `get_year(dt: String) -> Integer`: Extract year
- `get_month(dt: String) -> Integer`: Extract month
- `get_day(dt: String) -> Integer`: Extract day
- `get_hour(dt: String) -> Integer`: Extract hour
- `get_minute(dt: String) -> Integer`: Extract minute
- `get_second(dt: String) -> Integer`: Extract second
- `get_weekday(dt: String) -> Integer`: Extract weekday number
- `get_weekday_name(dt: String) -> String`: Extract weekday name
- `get_month_name(dt: String) -> String`: Extract month name

### Calendar Operations

- `is_leap_year(year: Integer) -> Boolean`: Check leap year
- `days_in_month(year: Integer, month: Integer) -> Integer`: Days in month
- `days_in_year(year: Integer) -> Integer`: Days in year
- `week_of_year(dt: String) -> Integer`: Week number
- `quarter_of_year(dt: String) -> Integer`: Quarter number

### Business Days

- `business_days_between(start: String, end: String) -> Integer`: Count business days
- `add_business_days(dt: String, days: Integer) -> String`: Add business days
- `subtract_business_days(dt: String, days: Integer) -> String`: Subtract business days
- `next_business_day(dt: String) -> String`: Next business day
- `previous_business_day(dt: String) -> String`: Previous business day
- `is_business_day(dt: String) -> Boolean`: Check if business day

### Timezone Operations

- `convert_timezone(dt: String, from_tz: String, to_tz: String) -> String`: Convert timezone
- `local_timezone() -> String`: Get local timezone
- `utc_now() -> String`: Get current UTC time
- `to_utc(dt: String, timezone: String) -> String`: Convert to UTC
- `from_utc(dt: String, timezone: String) -> String`: Convert from UTC

### Utility Functions

- `format_relative(dt: String) -> String`: Format relative time
- `format_duration(seconds: Number) -> String`: Format duration
- `parse_duration(duration: String) -> Number`: Parse duration
- `is_valid_date(date_string: String) -> Boolean`: Validate date
- `is_valid_time(time_string: String) -> Boolean`: Validate time
- `is_valid_datetime(datetime_string: String) -> Boolean`: Validate datetime

## Testing

The Time module includes comprehensive tests covering:

- Basic time operations and formatting
- Time arithmetic and comparisons
- Date component extraction
- Calendar operations and leap years
- Business day calculations
- Timezone conversions
- Duration formatting and parsing
- Date validation
- Error handling scenarios
- Performance with large date ranges

## Examples

See the `examples/basic/time_operations.runa` file for complete working examples of all Time module features. 