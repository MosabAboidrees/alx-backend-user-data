#!/usr/bin/env python3
"""
This module provides functions to filter and obfuscate
personal data fields in log messages.
"""

import re
from typing import List
import logging
from os import environ
import mysql.connector


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
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to filter specified fields."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to be redacted."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by filtering specified fields.
        Args:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: The formatted log message with specified fields redacted.
        """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
