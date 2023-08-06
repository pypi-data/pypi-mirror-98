def generate_feature(name, query, sql_dialect) -> dict:
    """

    :param name:
    :param query:
    :param sql_dialect:
    :return:
    """
    from .parse import parse_query
    ast, query_inputs, query_outputs, dependencies = parse_query(query=query, sql_dialect=sql_dialect,
                                                                 feature_name=name)
    feature = dict(
        name=name,
        inputs=query_inputs,
        outputs=query_outputs,
        dependencies=dependencies,
        query_ast=ast,
        allowed_dialects=get_allowed_dialects(query_ast=ast)
    )
    return feature


def get_allowed_dialects(query_ast):
    """

    :param query_ast:
    :return:
    """
    from .format import format_query
    from .dialects import list_dialects

    allowed_dialects = []
    for dialect in list_dialects():
        try:
            format_query(query_ast=query_ast, sql_dialect=dialect)
        except Exception:
            pass
        else:
            allowed_dialects.append(dialect)
    return allowed_dialects
