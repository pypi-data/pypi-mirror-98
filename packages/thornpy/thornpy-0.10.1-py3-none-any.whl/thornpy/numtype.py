"""numtype contains functions for checking the type of number that is contained within a string.
"""

def str_is_num(string):
    """Returns True if string is a number
    
    Parameters
    ----------
    string : str
        string possible representing a number
    
    Returns
    -------
    bool
        True if string represents a number

    """
    is_numeric = False
    if string:
        if string.replace('.', '', 1).replace('-','',1).isdigit():
            is_numeric = True    
    return is_numeric

def str_is_pos_num(string):
    """Returns True if string is a positive number
    
    Parameters
    ----------
    string : str
        string possible representing a number
    
    Returns
    -------
    bool
        True if string represents a positive number

    """
    is_numeric = False
    if string:
        # If the string is not empty check if it contains numbers
        if string.replace('.','',1).isdigit():
            is_numeric = True    
    return is_numeric


def str_is_float(numeric_string):
    """Returns true if the string is a float
    
    Arguments
    ---------
    string : str
        String representing a number
    
    Returns
    -------
    bool
        True if the string is a float
    """
    is_float = False
    if numeric_string:
        # If the string is not empty check if it contains numbers
        if numeric_string.replace('.','',1).replace('-','',1).isdigit():
            # If the string contains numbers, check if it contains a decimal
            if '.' in numeric_string:
                is_float = True
    return is_float

def str_is_int(numeric_string):
    """Returns true if the string is an integer
    
    Arguments
    ---------
    string : str
        String representing a number
    
    Returns
    -------
    bool
        True if the string is an integer
    """
    is_int = False
    if numeric_string:
        if numeric_string.replace('-','',1).isdigit():
            is_int = True
    return is_int

def str_is_pos_float(numeric_string):
    """Returns true if the string is a positive float
    
    Arguments
    ---------
    string : str 
        String representing a number
    
    Returns
    -------
    bool
        True if the string is a positive float
    """
    is_float = False
    if numeric_string:
        # If the string is not empty check if it contains numbers
        if numeric_string.replace('.','',1).isdigit():
            # If the string contains numbers, check if it contains a decimal
            if '.' in numeric_string:
                is_float = True
    return is_float

def str_is_pos_int(numeric_string):
    """Returns true if the string is a positive integer
    
    Arguments
    ---------
    string : str
        String representing a number
    
    Returns
    -------
    bool
        True if the string is a positive integer
    """
    is_int = False
    if numeric_string:
        if numeric_string.isdigit():
            is_int = True
    return is_int