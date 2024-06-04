#!/usr/bin/env python3
"""
Contains functions and classes for handling personal data securely.

This module provides functionalities for filtering sensitive information
from log messages, connecting to a MySQL database, and retrieving user data
while redacting Personally Identifiable Information (PII) fields.

Example:
    To use this module, simply run it as a script:
        $ python personal_data.py
"""

import logging
import os
import re
from typing import List
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redacts sensitive information from a log message.

    Args:
        fields (List[str]): List of sensitive fields to redact.
        redaction (str): The redaction string to replace sensitive data with.
        message (str): The log message to filter.
        separator (str): The separator used to separate fields in the message.

    Returns:
        str: The filtered log message with sensitive information redacted.
    """
    for f in fields:
        message = re.sub(rf"{f}=(.*?)\{separator}",
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter for redacting PII fields.

    Attributes:
        REDACTION (str): The string used for redacting sensitive data.
        FORMAT (str): The log message format.
        SEPARATOR (str): The separator used to separate fields in the log message.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter instance with a list of PII fields.

        Args:
            fields (List[str]): List of sensitive fields to redact.
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record while redacting PII fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with sensitive information redacted.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for logging user data.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main() -> None:
    """
    Retrieves user data from the database and prints it while redacting PII fields.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
