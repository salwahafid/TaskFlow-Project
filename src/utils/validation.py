import doctest

def valider_email(email: str) -> bool:
    """
    >>> valider_email("user@example.com")
    True

    >>> valider_email("invalid-email")
    False
    """

    import re
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

doctest.testmod(verbose=True)