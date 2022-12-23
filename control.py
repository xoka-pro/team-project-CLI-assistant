import re


def check_phone(text: str) -> bool:
    """validation phone

    Args:
        text (str): text phone for check

    Returns:
        bool: if match some mask: +380991112233 or 099-111-22-33 or 099-111-2233 or 0991112233
        or (099)1112233 or (099)111-22-33 or (099)111-2233
    """
    result = re.search(
        r"\d{3}\-\d{3}\-\d{2}\-\d{2}|\d{3}\-\d{3}\-\d{4}|\(\d{3}\)\d{3}\-\d{2}\-\d{2}|\(\d{3}\)\d{3}\-\d{4}|\(\d{3}\)\d{7}|\d{10}|\+\d{12}$", text)
    return not result is None


def check_email(text: str) -> bool:
    """validation email

    Args:
        text (str): text email for check

    Returns:
        bool: if first haven't !#$%^&*() and one @
        domens from 1-63 len and 1st domen name just letter 1-6 len
    """

    result = re.search(
        r"^(([A-Za-z0-9]+_+)|([A-Za-z0-9]+\-+)|([A-Za-z0-9]+\.+)|([A-Za-z0-9]+\++))*[A-Za-z0-9]+@((\w+\-+)|(\w+\.))*\w{1,63}\.[a-zA-Z]{2,6}$", text)
    return not result is None
