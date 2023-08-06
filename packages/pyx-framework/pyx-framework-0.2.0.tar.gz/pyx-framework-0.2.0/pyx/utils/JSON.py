

class JSON(dict):
    def __getattr__(self, key: str) -> object:
        if key in dir(self):
            return super().__getattribute__(key)
        result = self.get(key)
        if type(result) is JSON:
            return result
        if type(result) is dict:
            return JSON(result)
        if isinstance(result, list) and len(result) and type(result[0]) == dict:
            return [JSON(value) for value in result]
        return result

    def __setattr__(self, key: str, value: object):
        if key in dir(self):
            return super().__setattr__(key, value)
        self[key] = value

    def __delattr__(self, key: str):
        if self.get(key) is not None:
            return self.pop(key)

    def __or__(self, other):
        cls = type(self)
        return cls(super().__or__(other))
