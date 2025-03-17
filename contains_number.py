# Written by Conrad by referencing the below listed geeks for geeks article. It is used on the backend for checking if 
# name field input sent by a user contains a numerical character or not. 

def contains_number(s):
    """Check if the string contains any numerical character.
    source: https://www.geeksforgeeks.org/python-check-if-given-string-is-numeric-or-not/"""
    return any(char.isdigit() for char in s)
