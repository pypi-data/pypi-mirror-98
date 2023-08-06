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


def prune_ast(json, parent=None):
    """ Recursive function to remove partial or nulled values from the AST

    :param json: json query AST
    :param parent: the parent key of the ast
    :return: cleaned query AST
    """
    pruned = type(json)()
    if isinstance(json, dict):
        for k, v in json.items():
            child = prune_ast(json=v, parent=k)
            if child:
                pruned[k] = child
        pruned = validate_tree(k=parent, json=pruned)
    elif isinstance(json, list):
        for v in json:
            child = prune_ast(json=v, parent=None)
            if child:
                pruned.append(child)
        pruned = validate_tree(k=parent, json=pruned)
    else:
        if json is not None:
            pruned = json
    return pruned


def validate_tree(k, json):
    """ Validates whether the query ast has the required number of values

    :param k: the query key
    :param json: the query AST
    :return: None if invalid and the query_ast if valid.
    """
    from camtono.parser.parse import min_keys
    if k is None or len(json) >= min_keys.get(k, 1):
        return json
    else:
        return None


def set_value(val, **kwargs):
    """ Convenience function to set value for set_tree_value

    :param val: value to return
    :param kwargs: all other values
    :return: the value provided
    """
    return val


def set_tree_value(json, locations, replace_func=set_value, val=None, reverse_index=None, target=False):
    """ Set the

    :param json: dictionary
    :param locations: dictionary of the paths containing the location of a target value
    :param replace_func: function to apply when setting value receives val and json
    :param val: value to set
    :param reverse_index: location from the end of the tree where the replacement function should be applied
    :param target: boolean value to force value application
    :return: dictionary with the newly assigned values.
    """
    if locations and not target:
        current_index = None
        for k, v in locations.items():
            if k.isdigit():
                k = int(k)
            v, index = set_tree_value(json=json[k], locations=v, val=val, replace_func=replace_func,
                                      reverse_index=reverse_index)
            current_index = index + 1
            if reverse_index is not None and current_index == reverse_index:
                v, index = set_tree_value(json=json[k], locations=v, val=val, replace_func=replace_func, target=True,
                                          reverse_index=reverse_index)
            json[k] = v
        return json, current_index
    else:
        index = 0
        return replace_func(json=json, val=val), index
