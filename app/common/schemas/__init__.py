def omit(*fields):
    def dec(_class):
        _class.__fields__ = {
            key: field for key, field in _class.__fields__.items() if key not in fields
        }
        return _class

    return dec
