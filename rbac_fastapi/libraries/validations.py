import re


def number(data):
    return re.compile('^[0-9]+$').match(data)


def alphanumeric(data):
    return re.compile('^[0-9a-zA-z]+$').match(data)


def alphabetic(data):
    return re.compile('^[a-zA-z]+$').match(data)


def float_number(data):
    return re.compile(
        r'^[+]?\d*\.\d+([eE][+]?\d+)?$'
        ).match(str(data))


def currency_ron_euro(data):
    return re.compile(r'\b[12]\b').match(str(data))


def email(data):
    return re.compile(
        '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        ).match(data)


def product_name_validation(data):
    return re.compile(
        '^[ A-Za-z0-9-]+$'
    ).match(data)


def username(data):
    return re.compile(
        r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$'
        ).match(data)


def fullname(data):
    return re.compile(
        '[A-Za-z]{2,25}||\s[A-Za-z]{2,25}'
        ).match(data)


# Minimum eight characters, at least one letter,#$
#  one number and one special character:
def password(data):
    return re.compile(
        r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        ).match(data)


def servicename(data):
    return re.compile('^[a-zA-Z\s]+$').match(data)