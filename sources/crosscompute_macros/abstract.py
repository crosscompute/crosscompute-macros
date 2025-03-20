class Bag:

    def __init__(self, d=None):
        if d:
            for k, v in d.items():
                setattr(self, k, v)


class Clay:

    def __init__(self, instance=None, **kwargs):
        d = self.__dict__
        if instance:
            d.update(instance.__dict__)
        d.update(kwargs)
