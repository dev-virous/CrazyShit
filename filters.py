from re import compile

class filters:
    def regex(pattern):
        regex = compile(pattern)
        return lambda msg: regex.search(str(msg)) is not None