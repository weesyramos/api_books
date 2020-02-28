import re

def validate_name(name):
    if name:
        name = name.strip()
        validate_name_regex = '^[a-zA-z .]+$'
        if re.match(validate_name_regex, name):
            return name
    return None    


def validate_year(year):
    year = year.strip()
    validate_year_regex = '^\d{1,4}$'
    if re.match(validate_year_regex, year):
        return year
    return None