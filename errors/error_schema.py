"""
This file contains the error schema for the application
which is used to handle errors in the application
"""

class BaseException(Exception):
    reason = ""

    def __str__(self):
        return f'{self.reason}'

