def strtobool(value):
    value = value.lower()
    if value in ["y", "yes", "t", "true", "on", "1"]:
        result = True
    elif value in ["n", "no", "f", "false", "off", "0"]:
        result = False
    else:
        raise ValueError("invalid truth value '%s'".format(value))
    return result
