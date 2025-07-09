"""
Runa Standard Library - String Module

Provides string manipulation functions for Runa programs.
"""

import re

def length_of_string(text):
    """Get the length of a string."""
    return len(text)

def uppercase_string(text):
    """Convert string to uppercase."""
    return text.upper()

def lowercase_string(text):
    """Convert string to lowercase."""
    return text.lower()

def capitalize_string(text):
    """Capitalize the first letter of a string."""
    return text.capitalize()

def title_case_string(text):
    """Convert string to title case."""
    return text.title()

def trim_whitespace(text):
    """Remove whitespace from both ends of a string."""
    return text.strip()

def trim_left_whitespace(text):
    """Remove whitespace from the left end of a string."""
    return text.lstrip()

def trim_right_whitespace(text):
    """Remove whitespace from the right end of a string."""
    return text.rstrip()

def split_string(text, delimiter=" "):
    """Split a string by a delimiter."""
    return text.split(delimiter)

def join_strings(strings, separator=""):
    """Join a list of strings with a separator."""
    return separator.join(strings)

def replace_in_string(text, old, new, count=-1):
    """Replace occurrences of old with new in text."""
    return text.replace(old, new, count if count >= 0 else -1)

def contains_substring(text, substring):
    """Check if text contains substring."""
    return substring in text

def starts_with_substring(text, prefix):
    """Check if text starts with prefix."""
    return text.startswith(prefix)

def ends_with_substring(text, suffix):
    """Check if text ends with suffix."""
    return text.endswith(suffix)

def find_substring(text, substring, start=0):
    """Find the index of first occurrence of substring."""
    result = text.find(substring, start)
    return result if result >= 0 else None

def count_substring(text, substring):
    """Count occurrences of substring in text."""
    return text.count(substring)

def substring(text, start, end=None):
    """Extract a substring from start to end."""
    if end is None:
        return text[start:]
    return text[start:end]

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def is_empty_string(text):
    """Check if string is empty."""
    return len(text) == 0

def is_whitespace_only(text):
    """Check if string contains only whitespace."""
    return text.isspace()

def is_numeric_string(text):
    """Check if string represents a number."""
    try:
        float(text)
        return True
    except ValueError:
        return False

def is_alphabetic_string(text):
    """Check if string contains only alphabetic characters."""
    return text.isalpha()

def is_alphanumeric_string(text):
    """Check if string contains only alphanumeric characters."""
    return text.isalnum()

def repeat_string(text, count):
    """Repeat a string count times."""
    return text * count

def pad_left(text, width, fill_char=" "):
    """Pad string on the left to reach width."""
    return text.rjust(width, fill_char)

def pad_right(text, width, fill_char=" "):
    """Pad string on the right to reach width."""
    return text.ljust(width, fill_char)

def pad_center(text, width, fill_char=" "):
    """Center string within width."""
    return text.center(width, fill_char)

def match_pattern(text, pattern):
    """Check if text matches a regular expression pattern."""
    return bool(re.match(pattern, text))

def search_pattern(text, pattern):
    """Search for a regular expression pattern in text."""
    match = re.search(pattern, text)
    return match.group() if match else None

def find_all_patterns(text, pattern):
    """Find all occurrences of a pattern in text."""
    return re.findall(pattern, text)

def replace_pattern(text, pattern, replacement):
    """Replace pattern matches with replacement."""
    return re.sub(pattern, replacement, text)

def encode_string(text, encoding="utf-8"):
    """Encode string to bytes."""
    return text.encode(encoding)

def decode_bytes(data, encoding="utf-8"):
    """Decode bytes to string."""
    return data.decode(encoding)

def format_string(template, *args, **kwargs):
    """Format a string template with arguments."""
    return template.format(*args, **kwargs)

# Runa-style function names for natural language calling
get_length_of = length_of_string
convert_to_uppercase = uppercase_string
convert_to_lowercase = lowercase_string
convert_to_title_case = title_case_string
remove_whitespace = trim_whitespace
split_by_delimiter = split_string
join_with_separator = join_strings
replace_text = replace_in_string
check_if_contains = contains_substring
check_if_starts_with = starts_with_substring
check_if_ends_with = ends_with_substring
find_position_of = find_substring
count_occurrences = count_substring
extract_substring = substring
reverse_text = reverse_string
check_if_empty = is_empty_string
check_if_numeric = is_numeric_string
check_if_alphabetic = is_alphabetic_string
repeat_text = repeat_string
add_padding = pad_center
match_regular_expression = match_pattern
search_for_pattern = search_pattern
format_text = format_string