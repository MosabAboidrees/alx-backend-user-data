#!/usr/bin/env python3
"""
This module provides functions to filter and obfuscate
personal data fields in log messages.
"""

import re
from typing import List


def filter_datum(
                    fields: List[str],
                    redaction: str,
                    message: str,
                    separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The log message to filter.
        separator (str): Character that separates fields in the log message.
    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(rf"{field}=[^;]+", f"{field}={redaction}", message)
    return message
