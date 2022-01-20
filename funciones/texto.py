import re


def remove_spaces(text):
    """
    Removes spaces and changes them for ,
    :param text: str, input text where you want spaces removed
    :return: str, returns the text separated by , like word,word,word, etc.
    """
    text_list = text.split(',')  # splits the text in each space
    return ','.join(text_list)  # creates a new text with spaces changed with ,


def parse_text(text, regular_exp):
    """
    This function will parse the text using a regular expression and return the result
    :param text: str, the text where we are going to apply the regular expression
    :param regular_exp: str, regular expression
    :return: list, will have the matched regular expression if any
    """
    match = re.compile(regular_exp)
    result = match.search(text)
    return result
