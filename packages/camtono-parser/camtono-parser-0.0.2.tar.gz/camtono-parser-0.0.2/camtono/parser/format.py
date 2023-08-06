from .dialects import load_dialect_module
from .clean import strip_comments, encapsulate_variables, ENCODING_CHARACTER
from moz_sql_parser.formatting import Formatter as MozFormatter, escape


def format_query(query_ast, sql_dialect) -> str:
    """

    :param query_ast:
    :param sql_dialect:
    :return:
    """
    dialect = load_dialect_module(dialect_name=sql_dialect)
    formatted_query = dialect.format_query(query_ast=query_ast)

    formatted_query, variables = encapsulate_variables(
        query=formatted_query, encoding_character=ENCODING_CHARACTER,
        wrap_character='', skip_characters=len(ENCODING_CHARACTER)
    )
    formatted_query, variables = encapsulate_variables(
        query=formatted_query, encoding_character='"',
        wrap_character='', skip_characters=len(ENCODING_CHARACTER)
    )
    return formatted_query


class BaseFormatter(MozFormatter):
    """"""

    def _union(self, json, wrap=True):
        return "(" + self.union(json) + ")"

    def _union_all(self, json, wrap=True):
        return "(" + self.union_all(json) + ")"

    def union_distinct(self, json):
        return " UNION DISTINCT ".join(self.query(query) for query in json)

    def _union_distinct(self, json):
        return "(" + self.union_distinct(json=json) + ')'

    def _interval(self, json):
        return 'INTERVAL {0} {1}'.format(*json)

    def format(self, json):
        if "union" in json:
            return self.union(json["union"])
        elif "union_all" in json:
            return self.union_all(json["union_all"])
        elif "union_distinct" in json:
            return self.union_distinct(json["union_distinct"])
        else:
            return self.query(json)

    def _in(self, json):
        valid = self.dispatch(json[1])
        # `(10, 11, 12)` does not get parsed as literal, so it's formatted as
        # `10, 11, 12`. This fixes it.
        if not valid.startswith("("):
            valid = "({0})".format(valid)

        return "{0} IN {1}".format(self.dispatch(json[0]), valid)

    def _cast(self, json):
        _type = json[1]
        if isinstance(_type, dict):
            _type = list(_type.keys())[0]
        return "cast({0} AS {1})".format(json[0], _type)
