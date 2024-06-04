#!/usr/bin/env python3
"""
Demonstrates the usage of RedactingFormatter.

This script imports the RedactingFormatter class from the filtered_logger module
and uses it to format a log message containing sensitive information.

Example:
    $ python main.py
    Aug 22, 2021 10:10:10 AM - my_logger - INFO - name=Bob;email=REDACTED;ssn=REDACTED;password=REDACTED;
"""

import logging
import re

# Importing the RedactingFormatter class from filtered_logger module
RedactingFormatter = __import__('filtered_logger').RedactingFormatter

# Sample log message containing sensitive information
message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"

# Creating a LogRecord object with the log message
log_record = logging.LogRecord(
    "my_logger", logging.INFO, None, None, message, None, None)

# Creating an instance of RedactingFormatter with fields to be redacted
formatter = RedactingFormatter(fields=("email", "ssn", "password"))

# Formatting the log record with the RedactingFormatter and printing the result
print(formatter.format(log_record))
