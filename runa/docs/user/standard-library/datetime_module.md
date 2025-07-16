# Date Time Module

The Date Time module provides comprehensive date and time handling designed for AI-to-AI interfacing with nanosecond precision, natural language syntax, and extensive metadata support.

## Overview

The Date Time module is specifically designed for AI systems that need precise, reliable, and context-rich date and time operations. It provides nanosecond precision, flexible parsing, comprehensive validation, and rich metadata for AI reasoning and decision-making.

## Core Features

- **Nanosecond Precision**: All datetime operations support nanosecond precision for AI systems requiring exact timing
- **AI-Friendly Interfaces**: Natural language syntax that AIs can easily understand and generate
- **Flexible Parsing**: Multiple format support with intelligent format detection
- **Comprehensive Validation**: Extensive validation with detailed error messages for AI debugging
- **Rich Metadata**: Extensive metadata for AI reasoning and context understanding
- **Timezone Support**: Full timezone handling with DST awareness
- **Business Logic**: Business days, fiscal years, quarters, and calendar operations
- **Astronomical Data**: Moon phases, sunrise/sunset calculations
- **Performance Optimization**: Memory usage optimization and performance metrics
- **Serialization**: Multiple serialization formats for AI data exchange

## Basic Usage

### Getting Current Date/Time

```runa
Note: Get current datetime with nanosecond precision
:End Note

Let now be get current datetime with precision as "nanosecond"
Let today be get current date
Let current_time be get current time with precision as "nanosecond"

Note: AI systems can use these for precise timing and context
```

### Creating Date/Time Objects

```runa
Note: Create datetime objects with natural language syntax
:End Note

Let specific_datetime be create datetime with year as 2024 and month as 1 and day as 15 and hour as 14 and minute as 30 and second as 25 and nanosecond as 123456789
Let specific_date be create date with year as 2024 and month as 1 and day as 15
Let specific_time be create time with hour as 14 and minute as 30 and second as 25 and nanosecond as 123456789
```

### Parsing Date/Time Strings

```runa
Note: Parse datetime strings with flexible format detection
:End Note

Let parsed_datetime be parse datetime from "2024-01-15T14:30:25.123456789Z" with format as "iso"
Let parsed_date be parse date from "2024-01-15" with format as "iso"
Let parsed_time be parse time from "14:30:25.123456789" with format as "iso"

Note: AI systems can use flexible parsing for various input formats
Let flexible_parsed be parse datetime flexible from "January 15, 2024 at 2:30 PM"
```

### Formatting Date/Time

```runa
Note: Format datetime objects for AI-readable output
:End Note

Let formatted be format datetime specific_datetime with format as "iso"
Let human_readable be format datetime human readable specific_datetime with locale as "en_US"
Let custom_format be format datetime specific_datetime with format as "YYYY-MM-DD HH:mm:ss.SSSSSSSSS"
```

## API Reference

### Current Date/Time Operations

#### `get_current_datetime(precision: String) -> Dictionary[String, Any]`
Gets current datetime with specified precision.

**Parameters:**
- `precision`: Precision level ("second", "millisecond", "microsecond", "nanosecond")

**Returns:** Current datetime object with metadata

**Example:**
```runa
Let now be get current datetime with precision as "nanosecond"
Note: AI systems get precise timing for operations
```

#### `get_current_date() -> Dictionary[String, Any]`
Gets current date.

**Returns:** Current date object

#### `get_current_time(precision: String) -> Dictionary[String, Any]`
Gets current time with specified precision.

**Parameters:**
- `precision`: Precision level

**Returns:** Current time object

### Creation Operations

#### `create_datetime(year: Integer, month: Integer, day: Integer, hour: Integer, minute: Integer, second: Integer, nanosecond: Integer) -> Dictionary[String, Any]`
Creates datetime object with nanosecond precision.

**Parameters:**
- `year`: Year (1-9999)
- `month`: Month (1-12)
- `day`: Day (1-31)
- `hour`: Hour (0-23)
- `minute`: Minute (0-59)
- `second`: Second (0-59)
- `nanosecond`: Nanosecond (0-999999999)

**Returns:** Datetime object with validation metadata

#### `create_date(year: Integer, month: Integer, day: Integer) -> Dictionary[String, Any]`
Creates date object.

**Parameters:**
- `year`: Year (1-9999)
- `month`: Month (1-12)
- `day`: Day (1-31)

**Returns:** Date object

#### `create_time(hour: Integer, minute: Integer, second: Integer, nanosecond: Integer) -> Dictionary[String, Any]`
Creates time object with nanosecond precision.

**Parameters:**
- `hour`: Hour (0-23)
- `minute`: Minute (0-59)
- `second`: Second (0-59)
- `nanosecond`: Nanosecond (0-999999999)

**Returns:** Time object

### Parsing Operations

#### `parse_datetime(string: String, format: String) -> Dictionary[String, Any]`
Parses datetime string with specified format.

**Parameters:**
- `string`: Datetime string to parse
- `format`: Format specification ("iso", "rfc3339", "custom", etc.)

**Returns:** Parsed datetime object with parsing metadata

**Example:**
```runa
Let parsed be parse datetime from "2024-01-15T14:30:25.123456789Z" with format as "iso"
```

#### `parse_datetime_flexible(string: String) -> Dictionary[String, Any]`
Parses datetime string with intelligent format detection.

**Parameters:**
- `string`: Datetime string to parse

**Returns:** Parsed datetime object with detected format metadata

**Example:**
```runa
Let parsed be parse datetime flexible from "January 15, 2024 at 2:30 PM"
Let parsed2 be parse datetime flexible from "15/01/2024 14:30:25"
```

#### `parse_date(string: String, format: String) -> Dictionary[String, Any]`
Parses date string.

#### `parse_date_flexible(string: String) -> Dictionary[String, Any]`
Parses date string with intelligent format detection.

#### `parse_time(string: String, format: String) -> Dictionary[String, Any]`
Parses time string.

#### `parse_time_flexible(string: String) -> Dictionary[String, Any]`
Parses time string with intelligent format detection.

### Formatting Operations

#### `format_datetime(datetime: Dictionary[String, Any], format: String) -> String`
Formats datetime object to string.

**Parameters:**
- `datetime`: Datetime object to format
- `format`: Format specification

**Returns:** Formatted datetime string

#### `format_datetime_human_readable(datetime: Dictionary[String, Any], locale: String) -> String`
Formats datetime as human-readable string.

**Parameters:**
- `datetime`: Datetime object to format
- `locale`: Locale for formatting ("en_US", "en_GB", etc.)

**Returns:** Human-readable datetime string

**Example:**
```runa
Let readable be format datetime human readable now with locale as "en_US"
Note: Output: "January 15, 2024 at 2:30:25 PM"
```

#### `format_date(date: Dictionary[String, Any], format: String) -> String`
Formats date object.

#### `format_time(time: Dictionary[String, Any], format: String) -> String`
Formats time object.

### Component Access

#### `get_datetime_year(datetime: Dictionary[String, Any]) -> Integer`
Gets year component from datetime.

#### `get_datetime_month(datetime: Dictionary[String, Any]) -> Integer`
Gets month component from datetime.

#### `get_datetime_day(datetime: Dictionary[String, Any]) -> Integer`
Gets day component from datetime.

#### `get_datetime_hour(datetime: Dictionary[String, Any]) -> Integer`
Gets hour component from datetime.

#### `get_datetime_minute(datetime: Dictionary[String, Any]) -> Integer`
Gets minute component from datetime.

#### `get_datetime_second(datetime: Dictionary[String, Any]) -> Integer`
Gets second component from datetime.

#### `get_datetime_nanosecond(datetime: Dictionary[String, Any]) -> Integer`
Gets nanosecond component from datetime.

#### `get_datetime_weekday(datetime: Dictionary[String, Any]) -> Integer`
Gets weekday number (1=Monday, 7=Sunday).

#### `get_datetime_weekday_name(datetime: Dictionary[String, Any]) -> String`
Gets weekday name.

#### `get_datetime_week_number(datetime: Dictionary[String, Any]) -> Integer`
Gets week number of year.

#### `get_datetime_day_of_year(datetime: Dictionary[String, Any]) -> Integer`
Gets day of year (1-366).

### Calendar Operations

#### `is_datetime_leap_year(datetime: Dictionary[String, Any]) -> Boolean`
Checks if year is a leap year.

#### `get_datetime_quarter(datetime: Dictionary[String, Any]) -> Integer`
Gets quarter number (1-4).

#### `get_datetime_semester(datetime: Dictionary[String, Any]) -> Integer`
Gets semester number (1-2).

#### `get_datetime_fiscal_year(datetime: Dictionary[String, Any], fiscal_start_month: Integer) -> Integer`
Gets fiscal year.

#### `get_datetime_week_boundaries(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets week start and end dates.

#### `get_datetime_month_boundaries(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets month start and end dates.

#### `get_datetime_quarter_boundaries(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets quarter start and end dates.

#### `get_datetime_year_boundaries(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets year start and end dates.

### Timezone Operations

#### `get_datetime_timezone(datetime: Dictionary[String, Any]) -> String`
Gets timezone information.

#### `set_datetime_timezone(datetime: Dictionary[String, Any], timezone: String) -> Dictionary[String, Any]`
Sets timezone for datetime.

#### `convert_datetime_timezone(datetime: Dictionary[String, Any], target_timezone: String) -> Dictionary[String, Any]`
Converts datetime to different timezone.

#### `get_datetime_timezone_offset(datetime: Dictionary[String, Any], timezone: String) -> Integer`
Gets timezone offset in seconds.

#### `get_datetime_dst_info(datetime: Dictionary[String, Any], timezone: String) -> Dictionary[String, Any]`
Gets DST information.

#### `get_current_timezone() -> String`
Gets current system timezone.

#### `get_supported_timezones() -> List[String]`
Gets list of supported timezones.

#### `get_timezone_info(timezone: String) -> Dictionary[String, Any]`
Gets timezone information.

### Arithmetic Operations

#### `add_years_to_datetime(datetime: Dictionary[String, Any], years: Integer) -> Dictionary[String, Any]`
Adds years to datetime.

#### `add_months_to_datetime(datetime: Dictionary[String, Any], months: Integer) -> Dictionary[String, Any]`
Adds months to datetime.

#### `add_days_to_datetime(datetime: Dictionary[String, Any], days: Integer) -> Dictionary[String, Any]`
Adds days to datetime.

#### `add_hours_to_datetime(datetime: Dictionary[String, Any], hours: Integer) -> Dictionary[String, Any]`
Adds hours to datetime.

#### `add_minutes_to_datetime(datetime: Dictionary[String, Any], minutes: Integer) -> Dictionary[String, Any]`
Adds minutes to datetime.

#### `add_seconds_to_datetime(datetime: Dictionary[String, Any], seconds: Integer) -> Dictionary[String, Any]`
Adds seconds to datetime.

#### `add_nanoseconds_to_datetime(datetime: Dictionary[String, Any], nanoseconds: Integer) -> Dictionary[String, Any]`
Adds nanoseconds to datetime.

#### `subtract_years_from_datetime(datetime: Dictionary[String, Any], years: Integer) -> Dictionary[String, Any]`
Subtracts years from datetime.

#### `subtract_months_from_datetime(datetime: Dictionary[String, Any], months: Integer) -> Dictionary[String, Any]`
Subtracts months from datetime.

#### `subtract_days_from_datetime(datetime: Dictionary[String, Any], days: Integer) -> Dictionary[String, Any]`
Subtracts days from datetime.

#### `subtract_hours_from_datetime(datetime: Dictionary[String, Any], hours: Integer) -> Dictionary[String, Any]`
Subtracts hours from datetime.

#### `subtract_minutes_from_datetime(datetime: Dictionary[String, Any], minutes: Integer) -> Dictionary[String, Any]`
Subtracts minutes from datetime.

#### `subtract_seconds_from_datetime(datetime: Dictionary[String, Any], seconds: Integer) -> Dictionary[String, Any]`
Subtracts seconds from datetime.

#### `subtract_nanoseconds_from_datetime(datetime: Dictionary[String, Any], nanoseconds: Integer) -> Dictionary[String, Any]`
Subtracts nanoseconds from datetime.

### Duration Operations

#### `create_duration(years: Integer, months: Integer, days: Integer, hours: Integer, minutes: Integer, seconds: Integer, nanoseconds: Integer) -> Dictionary[String, Any]`
Creates duration object.

#### `calculate_duration_between(start_datetime: Dictionary[String, Any], end_datetime: Dictionary[String, Any], precision: String) -> Dictionary[String, Any]`
Calculates duration between two datetimes.

**Example:**
```runa
Let start be create datetime with year as 2024 and month as 1 and day as 1 and hour as 0 and minute as 0 and second as 0 and nanosecond as 0
Let end be create datetime with year as 2024 and month as 1 and day as 2 and hour as 12 and minute as 30 and second as 0 and nanosecond as 0
Let duration be calculate duration between start and end with precision as "nanosecond"
```

#### `get_duration_years(duration: Dictionary[String, Any]) -> Integer`
Gets years component from duration.

#### `get_duration_months(duration: Dictionary[String, Any]) -> Integer`
Gets months component from duration.

#### `get_duration_days(duration: Dictionary[String, Any]) -> Integer`
Gets days component from duration.

#### `get_duration_hours(duration: Dictionary[String, Any]) -> Integer`
Gets hours component from duration.

#### `get_duration_minutes(duration: Dictionary[String, Any]) -> Integer`
Gets minutes component from duration.

#### `get_duration_seconds(duration: Dictionary[String, Any]) -> Integer`
Gets seconds component from duration.

#### `get_duration_nanoseconds(duration: Dictionary[String, Any]) -> Integer`
Gets nanoseconds component from duration.

#### `add_duration_to_datetime(datetime: Dictionary[String, Any], duration: Dictionary[String, Any]) -> Dictionary[String, Any]`
Adds duration to datetime.

#### `subtract_duration_from_datetime(datetime: Dictionary[String, Any], duration: Dictionary[String, Any]) -> Dictionary[String, Any]`
Subtracts duration from datetime.

#### `format_duration_human_readable(duration: Dictionary[String, Any], locale: String) -> String`
Formats duration as human-readable string.

### Comparison Operations

#### `is_datetime_before(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any]) -> Boolean`
Checks if datetime1 is before datetime2.

#### `is_datetime_after(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any]) -> Boolean`
Checks if datetime1 is after datetime2.

#### `is_datetime_equal(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any]) -> Boolean`
Checks if datetimes are equal.

#### `is_datetime_between(datetime: Dictionary[String, Any], start_datetime: Dictionary[String, Any], end_datetime: Dictionary[String, Any]) -> Boolean`
Checks if datetime is between start and end.

#### `get_datetime_minimum(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets minimum of two datetimes.

#### `get_datetime_maximum(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets maximum of two datetimes.

#### `compare_datetime_precision(datetime1: Dictionary[String, Any], datetime2: Dictionary[String, Any], precision: String) -> Integer`
Compares datetimes at specified precision.

### Business Logic

#### `get_datetime_business_days_between(start_datetime: Dictionary[String, Any], end_datetime: Dictionary[String, Any], holidays: List[Dictionary[String, Any]]) -> Integer`
Calculates business days between datetimes.

#### `add_business_days_to_datetime(datetime: Dictionary[String, Any], business_days: Integer, holidays: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`
Adds business days to datetime.

#### `get_datetime_age(birth_datetime: Dictionary[String, Any], reference_datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Calculates age from birth datetime.

### Astronomical Operations

#### `get_datetime_moon_phase(datetime: Dictionary[String, Any]) -> String`
Gets moon phase for datetime.

#### `get_datetime_sunrise_sunset(datetime: Dictionary[String, Any], latitude: Number, longitude: Number) -> Dictionary[String, Any]`
Gets sunrise and sunset times.

### Validation Operations

#### `validate_datetime(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Validates datetime object.

#### `validate_date(date: Dictionary[String, Any]) -> Dictionary[String, Any]`
Validates date object.

#### `validate_time(time: Dictionary[String, Any]) -> Dictionary[String, Any]`
Validates time object.

#### `validate_datetime_format(string: String, format: String) -> Dictionary[String, Any]`
Validates datetime string format.

### Metadata Operations

#### `get_datetime_metadata(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets comprehensive metadata for datetime.

#### `get_date_metadata(date: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets comprehensive metadata for date.

#### `get_time_metadata(time: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets comprehensive metadata for time.

#### `get_duration_metadata(duration: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets comprehensive metadata for duration.

### Conversion Operations

#### `get_datetime_unix_timestamp(datetime: Dictionary[String, Any]) -> Number`
Gets Unix timestamp.

#### `create_datetime_from_unix_timestamp(timestamp: Number) -> Dictionary[String, Any]`
Creates datetime from Unix timestamp.

#### `get_datetime_epoch_milliseconds(datetime: Dictionary[String, Any]) -> Integer`
Gets epoch milliseconds.

#### `create_datetime_from_epoch_milliseconds(milliseconds: Integer) -> Dictionary[String, Any]`
Creates datetime from epoch milliseconds.

#### `get_datetime_epoch_nanoseconds(datetime: Dictionary[String, Any]) -> Integer`
Gets epoch nanoseconds.

#### `create_datetime_from_epoch_nanoseconds(nanoseconds: Integer) -> Dictionary[String, Any]`
Creates datetime from epoch nanoseconds.

#### `get_datetime_julian_day(datetime: Dictionary[String, Any]) -> Number`
Gets Julian day number.

#### `create_datetime_from_julian_day(julian_day: Number) -> Dictionary[String, Any]`
Creates datetime from Julian day.

### Utility Operations

#### `round_datetime_to_nearest(datetime: Dictionary[String, Any], unit: String) -> Dictionary[String, Any]`
Rounds datetime to nearest unit.

#### `truncate_datetime_to(datetime: Dictionary[String, Any], unit: String) -> Dictionary[String, Any]`
Truncates datetime to unit.

#### `create_datetime_range(start_datetime: Dictionary[String, Any], end_datetime: Dictionary[String, Any], step_duration: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Creates datetime range with step.

#### `serialize_datetime(datetime: Dictionary[String, Any], format: String) -> String`
Serializes datetime to string.

#### `deserialize_datetime(string: String, format: String) -> Dictionary[String, Any]`
Deserializes datetime from string.

#### `get_datetime_hash(datetime: Dictionary[String, Any], algorithm: String) -> String`
Gets hash of datetime.

### Performance Operations

#### `get_datetime_memory_usage(datetime: Dictionary[String, Any]) -> Integer`
Gets memory usage in bytes.

#### `optimize_datetime(datetime: Dictionary[String, Any]) -> Dictionary[String, Any]`
Optimizes datetime for memory usage.

#### `get_datetime_performance_metrics(operation: String) -> Dictionary[String, Any]`
Gets performance metrics for operation.

#### `benchmark_datetime_operations(operations: List[String]) -> Dictionary[String, Any]`
Benchmarks datetime operations.

## Advanced Examples

### AI Context Analysis

```runa
Note: AI systems can analyze datetime context for decision making
:End Note

Let now be get current datetime with precision as "nanosecond"
Let metadata be get datetime metadata now

Note: AI can analyze:
Note: - Time of day for user behavior patterns
Note: - Day of week for business logic
Note: - Season for contextual responses
Note: - Timezone for global operations
Note: - Precision for exact timing requirements
```

### Flexible Parsing for AI Input

```runa
Note: AI systems can handle various datetime input formats
:End Note

Let user_inputs be ["2024-01-15", "Jan 15, 2024", "15/01/2024", "January 15th, 2024"]
Let parsed_datetimes be []

For each input in user_inputs:
    Let parsed be parse datetime flexible from input
    Add parsed to parsed_datetimes
End For

Note: AI can now work with various user input formats
```

### Business Logic for AI Systems

```runa
Note: AI systems can handle business calendar logic
:End Note

Let start_date be create date with year as 2024 and month as 1 and day as 1
Let end_date be create date with year as 2024 and month as 1 and day as 31
Let holidays be [create date with year as 2024 and month as 1 and day as 1]

Let business_days be get datetime business days between start_date and end_date with holidays as holidays
Note: AI can calculate business timelines and schedules
```

### Precise Timing for AI Operations

```runa
Note: AI systems can measure precise operation timing
:End Note

Let start_time be get current datetime with precision as "nanosecond"
Note: Perform AI operation here
Let end_time be get current datetime with precision as "nanosecond"

Let duration be calculate duration between start_time and end_time with precision as "nanosecond"
Let human_duration be format duration human readable duration with locale as "en_US"

Note: AI operation took: human_duration
```

### Timezone Handling for Global AI

```runa
Note: AI systems can handle global timezone operations
:End Note

Let utc_time be get current datetime with precision as "nanosecond"
Let ny_time be convert datetime timezone utc_time to "America/New_York"
Let tokyo_time be convert datetime timezone utc_time to "Asia/Tokyo"

Note: AI can provide timezone-aware responses
Note: UTC: format datetime utc_time with format as "iso"
Note: NY: format datetime ny_time with format as "iso"
Note: Tokyo: format datetime tokyo_time with format as "iso"
```

## Error Handling

The Date Time module provides comprehensive error handling for AI systems:

```runa
Note: AI systems can handle datetime errors gracefully
:End Note

Try:
    Let invalid_datetime be create datetime with year as 2024 and month as 13 and day as 32 and hour as 25 and minute as 60 and second as 61 and nanosecond as 1000000000
    Note: This will fail validation
Catch error:
    Note: Invalid datetime detected: error
    Note: AI can provide helpful error messages and suggestions
End Try

Try:
    Let parsed be parse datetime from "invalid-date" with format as "iso"
    Note: This will fail parsing
Catch error:
    Note: Parsing error: error
    Note: AI can suggest correct formats or ask for clarification
End Try
```

## Performance Considerations

- Use appropriate precision levels for your use case
- Consider memory usage for large datetime collections
- Use caching for frequently accessed datetime calculations
- Optimize timezone conversions for global operations
- Monitor performance metrics for critical operations

## Security Considerations

- Validate all datetime inputs from external sources
- Use secure random number generation for datetime operations
- Handle timezone information securely
- Validate datetime formats to prevent injection attacks
- Use proper error handling to avoid information disclosure

## Testing

The Date Time module includes comprehensive tests covering:

- All datetime creation and parsing operations
- Timezone conversions and DST handling
- Arithmetic operations with edge cases
- Business logic and calendar operations
- Astronomical calculations
- Performance and memory optimization
- Error handling and validation
- AI-specific use cases

Run tests with:
```bash
runa test_datetime.runa
```

## Dependencies

The Date Time module depends on:
- System clock and timezone libraries
- Astronomical calculation libraries
- Timezone database
- Performance monitoring libraries
- Memory management utilities

## Future Enhancements

Planned features include:
- More astronomical calculations
- Advanced calendar systems
- Machine learning time series analysis
- Real-time datetime streaming
- Advanced timezone features
- Performance optimization
- AI-specific datetime patterns 