class MacroError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)


class WebError(MacroError):
    pass


class WebConnectionError(WebError):
    pass


class WebRequestError(WebError):
    pass
