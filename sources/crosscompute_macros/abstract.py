class Clay:

    def __init__(self, instance=None, **kwargs):
        d = self.__dict__
        if instance:
            d.update(instance.__dict__)
        d.update(kwargs)
