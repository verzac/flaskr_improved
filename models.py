class InvalidKeytagException(BaseException):
    pass


class HTMLLink:
    def __init__(self, label, href):
        self.href = href
        self.label = label

    def get_href(self):
        return self.href

    def get_label(self):
        return self.label
