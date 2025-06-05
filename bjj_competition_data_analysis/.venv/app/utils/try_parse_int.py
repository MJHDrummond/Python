def try_parse_int(value):
    """
    If input is INT, return value as INT, else return 0 (Zero)

    :param value: Any given input
    :return: INT
    """
    try:
        return int(value)
    except ValueError:
        return 0