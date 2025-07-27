# Runa Calendar Module Guide

The Runa Calendar module provides comprehensive date, time, and holiday management functionality. This module enables precise calendar calculations, date arithmetic, timezone handling, and international holiday recognition using Runa's natural language syntax.

## Overview

The calendar module consists of three main components:

- **core.runa**: Fundamental date/time operations and calculations
- **calendar.runa**: Calendar display and formatting utilities  
- **holidays.runa**: Holiday calculation and management system

## Core Date and Time Operations (`core.runa`)

### Date Creation and Validation

```runa
Note: Create and validate dates
Let today be create_date with year as 2024 and month as 6 and day as 15
Let invalid_date be create_date with year as 2024 and month as 13 and day as 1  Note: Throws error

Note: Check date validity
If is_valid_date with year as 2024 and month as 2 and day as 29:
    Display "February 29, 2024 is valid"  Note: Leap year

Note: Access date properties
Display "Year: " with message today["year"]
Display "Month: " with message today["month"] 
Display "Day: " with message today["day"]
Display "Day of week: " with message today["day_of_week"]    Note: 0=Monday, 6=Sunday
Display "Day of year: " with message today["day_of_year"]
Display "Week of year: " with message today["week_of_year"]
Display "Is leap year: " with message today["is_leap_year"]
```

### Leap Year Calculations

```runa
Note: Leap year determination
Let is_2024_leap be is_leap_year with year as 2024    Note: Returns true
Let is_2023_leap be is_leap_year with year as 2023    Note: Returns false
Let is_2000_leap be is_leap_year with year as 2000    Note: Returns true (divisible by 400)
Let is_1900_leap be is_leap_year with year as 1900    Note: Returns false (divisible by 100, not 400)

Note: Get days in month accounting for leap years
Let feb_days_leap be days_in_month with year as 2024 and month as 2     Note: Returns 29
Let feb_days_normal be days_in_month with year as 2023 and month as 2    Note: Returns 28
```

### Date Arithmetic

```runa
Note: Add and subtract days
Let base_date be create_date with year as 2024 and month as 6 and day as 15
Let future_date be add_days with date as base_date and days as 30
Let past_date be add_days with date as base_date and days as -10

Note: Add months and years
Let next_month be add_months with date as base_date and months as 1
Let next_year be add_years with date as base_date and years as 1

Note: Handle month-end edge cases
Let jan_31 be create_date with year as 2024 and month as 1 and day as 31  
Let feb_result be add_months with date as jan_31 and months as 1  Note: Becomes Feb 29 (leap year)

Note: Calculate differences between dates
Let date1 be create_date with year as 2024 and month as 6 and day as 15
Let date2 be create_date with year as 2024 and month as 6 and day as 20
Let difference be subtract_dates with date1 as date2 and date2 as date1  Note: Returns 5
```

### Time Creation and Operations  

```runa
Note: Create and manipulate time values
Let morning be create_time with hour as 9 and minute as 30 and second as 0
Let afternoon be create_time with hour as 14 and minute as 45 and second as 30

Note: Validate time values
If is_valid_time with hour as 25 and minute as 0 and second as 0:
    Display "Valid time"
Otherwise:
    Display "Invalid time - hour must be 0-23"

Note: Time arithmetic
Let time1 be create_time with hour as 10 and minute as 30 and second as 0
Let time2 be create_time with hour as 2 and minute as 15 and second as 30
Let combined_time be add_time with time1 as time1 and time2 as time2
Let time_difference be subtract_time with time1 as time1 and time2 as time2
```

### DateTime and Timezone Handling

```runa
Note: Create datetime with timezone
Let date_part be create_date with year as 2024 and month as 6 and day as 15
Let time_part be create_time with hour as 14 and minute as 30 and second as 0
Let utc_datetime be create_datetime with date as date_part and time as time_part and timezone as "UTC"

Note: Convert between timezones
Let est_datetime be convert_timezone with datetime as utc_datetime and target_timezone as "EST"
Display "UTC time: " with message utc_datetime["time"]["hour"]
Display "EST time: " with message est_datetime["time"]["hour"]

Note: Work with timestamps
Let current_moment be now
Let timestamp be current_moment["timestamp"]
Let recovered_datetime be from_timestamp with timestamp as timestamp and timezone as "UTC"
```

### Date Formatting and Parsing

```runa
Note: Format dates with various patterns
Let sample_date be create_date with year as 2024 and month as 6 and day as 15

Let iso_format be format_date with date as sample_date and format_string as "YYYY-MM-DD"
Display iso_format  Note: "2024-06-15"

Let us_format be format_date with date as sample_date and format_string as "MM/DD/YYYY"  
Display us_format  Note: "06/15/2024"

Let verbose_format be format_date with date as sample_date and format_string as "WWWW, MMMM DD, YYYY"
Display verbose_format  Note: "Saturday, June 15, 2024"

Note: Parse dates from strings
Let parsed_date be parse_date with date_string as "2024-06-15" and format_string as "YYYY-MM-DD"
```

### Calendar Boundaries and Ranges

```runa
Note: Get date ranges for periods
Let week_bounds be get_week_bounds with year as 2024 and week as 25
Display "Week starts: " with message format_date with date as week_bounds["start"] and format_string as "YYYY-MM-DD"
Display "Week ends: " with message format_date with date as week_bounds["end"] and format_string as "YYYY-MM-DD"

Let month_bounds be get_month_bounds with year as 2024 and month as 6
Let year_bounds be get_year_bounds with year as 2024
```

## Calendar Display (`calendar.runa`)

### Monthly Calendar Generation

```runa
Note: Create calendar display for any month
Let june_2024 be create_month_calendar with year as 2024 and month as 6

Note: Access calendar properties
Display "Calendar for: " with message june_2024["month_name"] with message " " with message june_2024["year"]
Display "First day of week: " with message june_2024["first_day_of_week"]
Display "Number of weeks: " with message june_2024["week_count"]

Note: Process calendar grid
For week_index from 0 to (length of june_2024["calendar_grid"] minus 1):
    Let week be june_2024["calendar_grid"][week_index]
    Let week_display be ""
    
    For each day in week:
        If day is equal to 0:
            Set week_display to week_display with message "   "  Note: Empty day
        Otherwise:
            If day is less than 10:
                Set week_display to week_display with message " " with message day with message " "
            Otherwise:
                Set week_display to week_display with message day with message " "
    
    Display week_display
```

### Calendar Formatting and Display

```runa
Note: Format calendar for display
Let march_2024 be create_month_calendar with year as 2024 and month as 3
Let format_options be dictionary with:
    "width" as 25,
    "show_week_numbers" as false,
    "highlight_today" as true

Let formatted_calendar be format_calendar with calendar_display as march_2024 and format_options as format_options
Display formatted_calendar

Note: The output will be:
Note:       March 2024
Note: Mon Tue Wed Thu Fri Sat Sun
Note:              1   2   3
Note:   4   5   6   7   8   9  10
Note:  11  12  13  14  15  16  17
Note:  18  19  20  21  22  23  24
Note:  25  26  27  28  29  30  31
```

### Custom Calendar Layouts

```runa
Note: Create custom calendar displays
Process called "create_mini_calendar" that takes year as Integer and month as Integer returns String:
    Let calendar_data be create_month_calendar with year as year and month as month
    Let result be calendar_data["month_name"] with message " " with message year with message "\n"
    
    Note: Add abbreviated weekday headers
    Set result to result with message "MTWTFSS\n"
    
    Note: Add calendar grid in compact format
    For each week in calendar_data["calendar_grid"]:
        For each day in week:
            If day is equal to 0:
                Set result to result with message " "
            Otherwise:
                Set result to result with message day modulo 10
        Set result to result with message "\n"
    
    Return result

Let mini_cal be create_mini_calendar with year as 2024 and month as 7
Display mini_cal
```

## Holiday Management (`holidays.runa`)

### Holiday Types and Creation

```runa
Note: Create different types of holidays
Let new_years be create_fixed_holiday with name as "New Year's Day" and month as 1 and day as 1 and category as "federal"
Let memorial_day be create_floating_holiday with name as "Memorial Day" and month as 5 and weekday as 1 and occurrence as -1 and category as "federal"
Let good_friday be create_easter_based_holiday with name as "Good Friday" and offset_days as -2 and category as "religious"
```

### Holiday Calendar Creation

```runa
Note: Create holiday calendars for different regions
Let us_holidays be create_holiday_calendar with year as 2024 and country_code as "US"
Let christian_holidays be create_holiday_calendar with year as 2024 and country_code as "Christian"
Let international_holidays be create_holiday_calendar with year as 2024 and country_code as "International"

Note: Display holiday information
Display "US Federal Holidays for 2024:"
For each holiday in us_holidays["holidays"]:
    Let formatted be format_date with date as holiday["date"] and format_string as "MMMM DD"
    Display holiday["name"] with message ": " with message formatted
```

### Holiday Queries and Calculations

```runa
Note: Check if specific dates are holidays
Let christmas_date be create_date with year as 2024 and month as 12 and day as 25
Let holiday_calendar be create_holiday_calendar with year as 2024 and country_code as "US"

If is_holiday with date as christmas_date and calendar as holiday_calendar:
    Let holiday_info be get_holiday_on_date with date as christmas_date and calendar as holiday_calendar
    Display "Today is: " with message holiday_info["name"]

Note: Find holidays in specific periods
Let december_holidays be get_holidays_in_month with year as 2024 and month as 12 and calendar as holiday_calendar
Let year_end_holidays be get_holidays_in_range with start_date as create_date with year as 2024 and month as 12 and day as 1 and end_date as create_date with year as 2024 and month as 12 and day as 31 and calendar as holiday_calendar
```

### Business Day Calculations

```runa
Note: Calculate business days
Let test_date be create_date with year as 2024 and month as 7 and day as 4  Note: Independence Day
Let holiday_cal be create_holiday_calendar with year as 2024 and country_code as "US"

If is_business_day with date as test_date and calendar as holiday_cal:
    Display "This is a business day"
Otherwise:
    Display "This is not a business day (weekend or holiday)"

Note: Get all business days in a month
Let june_business_days be get_business_days_in_month with year as 2024 and month as 6 and calendar as holiday_cal
Display "Business days in June 2024: " with message length of june_business_days
```

### Custom Holiday Management

```runa
Note: Add custom holidays to calendar
Let company_calendar be create_holiday_calendar with year as 2024 and country_code as "US"
Let founder_day be create_date with year as 2024 and month as 8 and day as 15

Let updated_calendar be add_custom_holiday with calendar as company_calendar and name as "Founder's Day" and date as founder_day and category as "company"

Note: Verify custom holiday was added
If is_holiday with date as founder_day and calendar as updated_calendar:
    Display "Founder's Day is now recognized as a company holiday"
```

### Easter and Religious Holiday Calculations

```runa
Note: Calculate Easter and related holidays
Let easter_2024 be calculate_easter with year as 2024
Display "Easter 2024: " with message format_date with date as easter_2024 and format_string as "MMMM DD, YYYY"

Let easter_2025 be calculate_easter with year as 2025
Display "Easter 2025: " with message format_date with date as easter_2025 and format_string as "MMMM DD, YYYY"

Note: Calculate holidays relative to Easter
Let palm_sunday be add_days with date as easter_2024 and days as -7
Let maundy_thursday be add_days with date as easter_2024 and days as -3
Let easter_monday be add_days with date as easter_2024 and days as 1
```

### Advanced Holiday Operations

```runa
Note: Analyze holiday patterns and statistics
Let holiday_calendar be create_holiday_calendar with year as 2024 and country_code as "US"

Let total_holidays be count_holidays_in_year with calendar as holiday_calendar
Let weekend_holidays be count_weekend_holidays with calendar as holiday_calendar

Display "Total holidays: " with message total_holidays
Display "Weekend holidays: " with message weekend_holidays
Display "Weekday holidays: " with message (total_holidays minus weekend_holidays)

Note: Find next and previous holidays
Let today be create_date with year as 2024 and month as 6 and day as 15
Let next_holiday be get_next_holiday with current_date as today and calendar as holiday_calendar
Let previous_holiday be get_previous_holiday with current_date as today and calendar as holiday_calendar

If next_holiday is not None:
    Display "Next holiday: " with message next_holiday["name"]
If previous_holiday is not None:
    Display "Previous holiday: " with message previous_holiday["name"]
```

## Integration Examples

### Complete Calendar Application

```runa
Note: Build a comprehensive calendar application
Process called "create_calendar_report" that takes year as Integer and month as Integer returns String:
    Let calendar_display be create_month_calendar with year as year and month as month
    Let holiday_calendar be create_holiday_calendar with year as year and country_code as "US"
    
    Let report be list containing
    Add "CALENDAR REPORT" to report
    Add "=================" to report
    Add "" to report
    
    Note: Add calendar header
    Add calendar_display["month_name"] with message " " with message year to report
    Add "" to report
    
    Note: Add formatted calendar
    Let formatted_cal be format_calendar with calendar_display as calendar_display and format_options as dictionary with "width" as 25
    Add formatted_cal to report
    Add "" to report
    
    Note: Add holiday information
    Let month_holidays be get_holidays_in_month with year as year and month as month and calendar as holiday_calendar
    If length of month_holidays is greater than 0:
        Add "HOLIDAYS THIS MONTH:" to report
        Add "====================" to report
        For each holiday in month_holidays:
            Let holiday_text be format_holiday with holiday as holiday and format_type as "long"
            Add holiday_text to report
        Add "" to report
    
    Note: Add business day analysis
    Let business_days be get_business_days_in_month with year as year and month as month and calendar as holiday_calendar
    Add "BUSINESS DAYS: " with message length of business_days to report
    Add "TOTAL DAYS: " with message days_in_month with year as year and month as month to report
    
    Note: Add weekend count
    Let weekend_count be 0
    For day from 1 to days_in_month with year as year and month as month:
        Let check_date be create_date with year as year and month as month and day as day
        Let weekday be check_date["day_of_week"]
        If weekday is equal to 5 or weekday is equal to 6:  Note: Saturday or Sunday
            Set weekend_count to weekend_count plus 1
    
    Add "WEEKEND DAYS: " with message weekend_count to report
    
    Return join_lines with lines as report

Note: Generate report for June 2024
Let june_report be create_calendar_report with year as 2024 and month as 6
Display june_report
```

### Date Range Operations

```runa
Note: Work with date ranges and intervals
Process called "analyze_date_range" that takes start_date as Date and end_date as Date returns Dictionary[String, Any]:
    Let total_days be subtract_dates with date1 as end_date and date2 as start_date plus 1
    Let holiday_calendar be create_holiday_calendar with year as start_date["year"] and country_code as "US"
    
    Let business_day_count be 0
    Let weekend_count be 0
    Let holiday_count be 0
    
    Let current_day be 0
    While current_day is less than total_days:
        Let check_date be add_days with date as start_date and days as current_day
        Let weekday be check_date["day_of_week"]
        
        If weekday is equal to 5 or weekday is equal to 6:
            Set weekend_count to weekend_count plus 1
        Otherwise if is_holiday with date as check_date and calendar as holiday_calendar:
            Set holiday_count to holiday_count plus 1
        Otherwise:
            Set business_day_count to business_day_count plus 1
        
        Set current_day to current_day plus 1
    
    Return dictionary with:
        "total_days" as total_days,
        "business_days" as business_day_count,
        "weekend_days" as weekend_count,
        "holiday_days" as holiday_count,
        "start_date" as start_date,
        "end_date" as end_date

Note: Analyze a quarter
Let q2_start be create_date with year as 2024 and month as 4 and day as 1
Let q2_end be create_date with year as 2024 and month as 6 and day as 30
Let q2_analysis be analyze_date_range with start_date as q2_start and end_date as q2_end

Display "Q2 2024 Analysis:"
Display "Total days: " with message q2_analysis["total_days"]
Display "Business days: " with message q2_analysis["business_days"]
Display "Weekend days: " with message q2_analysis["weekend_days"]
Display "Holiday days: " with message q2_analysis["holiday_days"]
```

### Time Zone Management

```runa
Note: Handle multiple time zones in business applications
Process called "schedule_global_meeting" that takes local_time as DateTime and participant_zones as List[String] returns List[Dictionary[String, Any]]:
    Let meeting_times be list containing
    
    For each zone in participant_zones:
        Let converted_time be convert_timezone with datetime as local_time and target_timezone as zone
        Let meeting_info be dictionary with:
            "timezone" as zone,
            "local_time" as format_date with date as converted_time["date"] and format_string as "YYYY-MM-DD",
            "local_hour" as converted_time["time"]["hour"],
            "local_minute" as converted_time["time"]["minute"],
            "is_business_hours" as (converted_time["time"]["hour"] is greater than or equal to 9 and converted_time["time"]["hour"] is less than 18)
        
        Add meeting_info to meeting_times
    
    Return meeting_times

Note: Schedule a meeting
Let base_date be create_date with year as 2024 and month as 6 and day as 15
Let base_time be create_time with hour as 14 and minute as 0 and second as 0  Note: 2 PM
Let utc_meeting be create_datetime with date as base_date and time as base_time and timezone as "UTC"

Let zones be list containing "UTC", "EST", "PST", "CET", "JST"
Let meeting_schedule be schedule_global_meeting with local_time as utc_meeting and participant_zones as zones

For each meeting_time in meeting_schedule:
    Display meeting_time["timezone"] with message ": " with message meeting_time["local_hour"] with message ":" with message meeting_time["local_minute"] with message " (Business hours: " with message meeting_time["is_business_hours"] with message ")"
```

## Testing Your Code

The calendar module includes comprehensive test coverage. Run the test suite to verify functionality:

```bash
cd runa/
python -m pytest tests/unit/stdlib/test_calendar.runa -v
```

Key test categories:
- Date creation and validation
- Leap year calculations
- Day of week algorithms
- Date arithmetic accuracy
- Time zone conversions
- Holiday calculations
- Calendar display formatting
- Business day logic

## Performance Considerations

### Efficient Date Operations

```runa
Note: Cache frequently used date calculations
Let date_cache be dictionary containing

Process called "get_cached_day_of_week" that takes year as Integer and month as Integer and day as Integer returns Integer:
    Let cache_key be "" with message year with message "-" with message month with message "-" with message day
    
    If date_cache contains key cache_key:
        Return date_cache[cache_key]
    
    Let date_obj be create_date with year as year and month as month and day as day
    Set date_cache[cache_key] to date_obj["day_of_week"]
    Return date_obj["day_of_week"]
```

### Bulk Operations

```runa
Note: Process multiple dates efficiently
Process called "generate_business_days_bulk" that takes start_year as Integer and end_year as Integer returns List[Date]:
    Let all_business_days be list containing
    
    For year from start_year to end_year:
        Let year_calendar be create_holiday_calendar with year as year and country_code as "US"
        
        For month from 1 to 12:
            Let month_business_days be get_business_days_in_month with year as year and month as month and calendar as year_calendar
            For each business_date in month_business_days:
                Add business_date to all_business_days
    
    Return all_business_days
```

## Advanced Features

### Custom Calendar Systems

```runa
Note: Implement custom calendar systems
Process called "create_fiscal_year_calendar" that takes fiscal_start_month as Integer returns Dictionary[String, Any]:
    Let fiscal_calendar be dictionary with:
        "start_month" as fiscal_start_month,
        "quarters" as list containing,
        "year_length" as 12

    Note: Define fiscal quarters
    For quarter from 1 to 4:
        Let quarter_start be ((fiscal_start_month plus ((quarter minus 1) times 3) minus 1) modulo 12) plus 1
        Let quarter_months be list containing
        
        For i from 0 to 2:
            Let month_num be ((quarter_start plus i minus 1) modulo 12) plus 1
            Add month_num to quarter_months
        
        Add quarter_months to fiscal_calendar["quarters"]
    
    Return fiscal_calendar

Let fy_calendar be create_fiscal_year_calendar with fiscal_start_month as 7  Note: July start
```

### Holiday Pattern Analysis

```runa
Note: Analyze holiday patterns across multiple years
Process called "analyze_holiday_patterns" that takes start_year as Integer and end_year as Integer returns Dictionary[String, Any]:
    Let pattern_analysis be dictionary with:
        "weekend_holidays" as dictionary containing,
        "monthly_distribution" as dictionary containing,
        "total_years_analyzed" as end_year minus start_year plus 1
    
    For year from start_year to end_year:
        Let year_holidays be create_holiday_calendar with year as year and country_code as "US"
        
        For each holiday in year_holidays["holidays"]:
            Let month_name be core.MONTH_NAMES[holiday["date"]["month"] minus 1]
            Let weekday be holiday["date"]["day_of_week"]
            
            Note: Track monthly distribution
            If pattern_analysis["monthly_distribution"] contains key month_name:
                Set pattern_analysis["monthly_distribution"][month_name] to pattern_analysis["monthly_distribution"][month_name] plus 1
            Otherwise:
                Set pattern_analysis["monthly_distribution"][month_name] to 1
            
            Note: Track weekend holidays
            If weekday is equal to 5 or weekday is equal to 6:
                If pattern_analysis["weekend_holidays"] contains key holiday["name"]:
                    Set pattern_analysis["weekend_holidays"][holiday["name"]] to pattern_analysis["weekend_holidays"][holiday["name"]] plus 1
                Otherwise:
                    Set pattern_analysis["weekend_holidays"][holiday["name"]] to 1
    
    Return pattern_analysis

Let holiday_patterns be analyze_holiday_patterns with start_year as 2020 and end_year as 2030
```

The Runa Calendar module provides powerful, accurate date and time functionality suitable for business applications, scheduling systems, and international software. Its natural language syntax makes complex calendar operations intuitive while maintaining the precision required for professional applications.