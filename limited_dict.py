

class LimitedDict(dict):
    def __init__(self, _max_len: int) -> None:
        if _max_len < 1:
            raise ValueError("Length must be a positive number.")
        super().__init__()
        self._max_len = _max_len

    def __setitem__(self, key: object, item: object) -> None:
        if self.__len__() != 0 and self.__len__() == self._max_len:
            self.pop(next(iter(self)))
        super().__setitem__(key, item)
