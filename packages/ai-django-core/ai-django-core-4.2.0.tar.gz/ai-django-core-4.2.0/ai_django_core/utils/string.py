import datetime
import os

from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat

from ai_django_core.utils import datetime_format


def distinct(not_distinct_list: list) -> list:
    """
    Returns a list with no duplicate elements
    """
    return list(set(not_distinct_list))


def slugify_file_name(file_name: str, length: int = 40) -> str:
    """
    Slugify the given file name
    """
    from django.template.defaultfilters import slugify
    from django.utils.encoding import smart_str
    name, ext = os.path.splitext(file_name)
    name = smart_str(slugify(name).replace('-', '_'))
    ext = smart_str(slugify(ext))
    result = '%s%s%s' % (name[:length], "." if ext else "", ext)
    return result


def smart_truncate(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Returns a string of at most `max_length` characters, cutting
    only at word-boundaries. If the string was truncated, `suffix`
    will be appended.
    In comparison to djangos defaultfilter `truncatechars` this method does NOT break words and you
    can choose a custom suffix.
    # todo write test & rename (?) & add filter?
    """

    if text is None:
        return ''

    # Return the string itself if length is smaller or equal to the limit
    if len(text) <= max_length:
        return text

    # Cut the string
    value = text[:max_length]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + suffix


def float_to_string(value: float, replacement: str = "0,00") -> str:
    """
    Converts a float to a properly formatted string value
    """
    return ("%.2f" % value).replace('.', ',') if value is not None else replacement


def date_to_string(value: datetime.date, replacement: str = "-", str_format: str = "%d.%m.%Y") -> str:
    return value.strftime(str_format) if value is not None else replacement


def datetime_to_string(value: datetime.datetime, replacement: str = "-", str_format: str = "%d.%m.%Y %H:%M") -> str:
    return datetime_format(value, str_format) if value is not None else replacement


def number_to_string(value, decimal_digits: int = 0, replacement: str = "-") -> str:
    return intcomma(floatformat(value, decimal_digits)) if value is not None else replacement


def string_or_none_to_string(value, replacement: str = "-") -> str:
    return value if value is not None else replacement


def encode_to_xml(text: str) -> str:
    text_str = str(text)
    text_str = text_str.replace('&', '&amp;')
    text_str = text_str.replace('<', '&lt;')
    text_str = text_str.replace('>', '&gt;')

    return text_str
