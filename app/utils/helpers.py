"""
Helper Utilities Module

Contains reusable helper functions for the application.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
import calendar
import json
from app.utils.constants import DATE_FORMAT, DISPLAY_DATE_FORMAT
from app.logger import get_logger

logger = get_logger(__name__)


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format amount as currency string.

    Args:
        amount: Amount to format
        currency: Currency code

    Returns:
        Formatted currency string
    """
    from app.utils.constants import CURRENCY_SYMBOLS

    symbol = CURRENCY_SYMBOLS.get(currency, "$")
    return f"{symbol}{amount:,.2f}"


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse date string to datetime object.

    Args:
        date_string: Date string in YYYY-MM-DD format

    Returns:
        Datetime object or None
    """
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except (ValueError, TypeError):
        logger.warning(f"Failed to parse date: {date_string}")
        return None


def format_date(date_obj: datetime, format_style: str = "display") -> str:
    """
    Format datetime object to string.

    Args:
        date_obj: Datetime object
        format_style: 'display' or 'iso'

    Returns:
        Formatted date string
    """
    if not date_obj:
        return ""

    if format_style == "display":
        return date_obj.strftime(DISPLAY_DATE_FORMAT)
    else:
        return date_obj.strftime(DATE_FORMAT)


def get_date_range_for_month(month: int, year: int) -> Tuple[datetime, datetime]:
    """
    Get start and end dates for a month.

    Args:
        month: Month number (1-12)
        year: Year

    Returns:
        Tuple of (start_date, end_date)
    """
    first_day = datetime(year, month, 1)
    last_day = datetime(
        year,
        month,
        calendar.monthrange(year, month)[1],
        23,
        59,
        59
    )
    return first_day, last_day


def get_date_range_for_year(year: int) -> Tuple[datetime, datetime]:
    """
    Get start and end dates for a year.

    Args:
        year: Year

    Returns:
        Tuple of (start_date, end_date)
    """
    first_day = datetime(year, 1, 1)
    last_day = datetime(year, 12, 31, 23, 59, 59)
    return first_day, last_day


def round_currency(amount: float, places: int = 2) -> float:
    """
    Round currency amount to specified places.

    Args:
        amount: Amount to round
        places: Decimal places

    Returns:
        Rounded amount
    """
    try:
        decimal_amount = Decimal(str(amount))
        rounded = decimal_amount.quantize(
            Decimal(10) ** -places,
            rounding=ROUND_HALF_UP
        )
        return float(rounded)
    except Exception:
        return round(amount, places)


def calculate_percentage(value: float, total: float) -> float:
    """
    Calculate percentage of value from total.

    Args:
        value: Value
        total: Total

    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)


def group_by_category(
    items: List[Dict[str, Any]],
    category_key: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group items by category.

    Args:
        items: List of items to group
        category_key: Key to group by

    Returns:
        Dictionary with categories as keys
    """
    grouped = {}
    for item in items:
        category = item.get(category_key, "Other")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped


def sum_amounts(items: List[Dict[str, Any]], amount_key: str) -> float:
    """
    Sum amounts from list of items.

    Args:
        items: List of items
        amount_key: Key containing amount

    Returns:
        Sum of all amounts
    """
    total = 0.0
    for item in items:
        try:
            total += float(item.get(amount_key, 0))
        except (ValueError, TypeError):
            continue
    return round_currency(total)


def get_months_list(months_back: int = 12) -> List[Tuple[int, int, str]]:
    """
    Get list of months.

    Args:
        months_back: Number of months back to include

    Returns:
        List of (year, month, display_name) tuples
    """
    months = []
    today = datetime.now()

    for i in range(months_back):
        current_date = today - timedelta(days=30 * i)
        year = current_date.year
        month = current_date.month
        month_name = current_date.strftime("%B %Y")
        months.append((year, month, month_name))

    return months


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.

    Args:
        filename: Original filename

    Returns:
        Safe filename
    """
    from app.security import input_sanitizer
    return input_sanitizer.sanitize_filename(filename)


def generate_report_filename(report_type: str, extension: str) -> str:
    """
    Generate report filename with timestamp.

    Args:
        report_type: Type of report
        extension: File extension

    Returns:
        Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{report_type}_report_{timestamp}{extension}"


def retry_on_exception(
    func,
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: Tuple = (Exception,)
):
    """
    Retry a function on exception.

    Args:
        func: Function to retry
        max_attempts: Maximum attempts
        delay: Delay between attempts in seconds
        exceptions: Tuple of exceptions to catch

    Returns:
        Function result or None
    """
    import time

    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            if attempt < max_attempts - 1:
                logger.warning(
                    f"Attempt {attempt + 1} failed: {str(e)}. "
                    f"Retrying in {delay} seconds..."
                )
                time.sleep(delay)
            else:
                logger.error(f"All {max_attempts} attempts failed: {str(e)}")
                raise


def serialize_to_json(obj: Any) -> str:
    """
    Serialize object to JSON string.

    Args:
        obj: Object to serialize

    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, default=str, indent=2)
    except Exception as e:
        logger.error(f"JSON serialization error: {str(e)}")
        return "{}"


def deserialize_from_json(json_string: str) -> Optional[Any]:
    """
    Deserialize JSON string to object.

    Args:
        json_string: JSON string

    Returns:
        Deserialized object or None
    """
    try:
        return json.loads(json_string)
    except Exception as e:
        logger.error(f"JSON deserialization error: {str(e)}")
        return None


def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Truncate string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def compare_dates(date1: datetime, date2: datetime) -> int:
    """
    Compare two dates.

    Args:
        date1: First date
        date2: Second date

    Returns:
        -1 if date1 < date2, 0 if equal, 1 if date1 > date2
    """
    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    else:
        return 0


def get_time_difference_string(date1: datetime, date2: datetime) -> str:
    """
    Get human-readable time difference.

    Args:
        date1: First date
        date2: Second date

    Returns:
        Time difference string
    """
    diff = abs((date2 - date1).total_seconds())

    if diff < 60:
        return "just now"
    elif diff < 3600:
        minutes = int(diff / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif diff < 86400:
        hours = int(diff / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = int(diff / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
