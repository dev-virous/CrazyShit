from json import dumps

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def __default__(obj: "Parser"):
        return {
            **{
                attr: (
                    getattr(obj, attr)
                )
                for attr in obj.__dict__
                if getattr(obj, attr) is not None
            }
        } if not isinstance(obj, set) else [i for i in obj]

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Parser.__default__, ensure_ascii=False)

class dtc(Parser):
    def __init__(self, dic: dict):
        super().__init__()
        __ = False
        while not __:
            try:
                for i in dic:
                    if isinstance(dic[i], dict):
                        setattr(self, i, dtc(dic[i]))
                    elif isinstance(dic[i], list):
                        setattr(self, i, [dtc(x) if isinstance(x, dict) else x for x in dic[i]])
                    else:
                        setattr(self, i, dic[i])
                __ = True
            except Exception:
                pass