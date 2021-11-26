# This is a sample Python script.
import re
import subprocess
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def parse_text(text, regular_exp):
    """
    This function will parse the text using a regular expression and return the result
    :param regular_exp: str, regular exprenssion
    :return: list, will have the matched regular expression if any
    """
    match = re.compile(regular_exp)
    result = match.search(text)
    return result