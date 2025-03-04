def contains_number(s):
    """Check if the string contains any numerical character.
    source: https://www.geeksforgeeks.org/python-check-if-given-string-is-numeric-or-not/"""
    return any(char.isdigit() for char in s)
