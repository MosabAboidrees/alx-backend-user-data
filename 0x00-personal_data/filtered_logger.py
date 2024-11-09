#!/usr/bin/env python3
"""
Module for logging with obfuscation of sensitive information.
Provides functions and classes to handle sensitive data logging.
"""
import re
import logging
from os import environ
from typing import List
import mysql.connector

# Define PII fields that need obfuscation
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Replacement string for obfuscation.
        message (str): Log message to filter.
        separator (str): Field separator in the log message.
    Returns:
        str: Obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to filter specified fields in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize formatter with fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record by filtering specified fields."""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logger with a custom formatter for PII fields.
    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to the MySQL database securely using environment variables.
    Returns:
        connection.MySQLConnection: MySQL connection object.
    """
    return mysql.connector.connect(
        username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password = os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    )
