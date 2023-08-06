import re

ENCODING_CHARACTER = "'"


def clean_query(query, sql_dialect) -> str:
    """

    :param query:
    :param sql_dialect:
    :return:
    """
    cleaned_query = strip_comments(query=query)
    cleaned_query = clean_spaces(query=cleaned_query)
    return cleaned_query.lower()


def clean_spaces(query) -> str:
    """

    :param query:
    :return:
    """
    cleaned_query = re.sub('\s+', ' ', query)
    cleaned_query = re.sub('\(\s', '(', cleaned_query)
    cleaned_query = re.sub('\s\)', ')', cleaned_query)
    return cleaned_query.strip()


def strip_comments(query) -> str:
    """

    :param query:
    :return:
    """
    return re.sub('(([\s-]+-).+\n)|(([\s\#]+\#).+\n)', ' ', query)


def encapsulate_variables(query, encoding_character='', wrap_character="'", encoded=False, skip_characters=0,
                          feature_name=None):
    """

    :param query:
    :param encoding_character:
    :param wrap_character:
    :param encoded:
    :param skip_characters:
    :param feature_name:
    :return:
    """
    if encoded and encoding_character:
        encoding_character = '\\' + encoding_character
    regex = '(' + encoding_character + '\{\S+\}' + encoding_character + ')'
    variables = set()

    for match in re.findall(regex, query):
        new_name = match
        if new_name not in variables:
            new_string = wrap_character + new_name[skip_characters:len(new_name) - skip_characters] + wrap_character
            query = query.replace(
                match,
                new_string
            )
            variables.add(new_name)
    return query, variables
