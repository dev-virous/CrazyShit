from re import compile


class filters:
    def regex(pattern):
        """regix compiler to compile the text message if matching the given pattern"""
        regex = compile(pattern)
        return lambda msg: regex.search(str(msg)) is not None
