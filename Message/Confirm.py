import json

class Confirm(object):

    def __init__(self, builder):
        self.__title = builder._title
        self.__text = builder._text
        self.__ok_text = builder._ok_text
        self.__dismiss_text = builder._dismiss_text

    def to_dict(self):
        d = {}
        if self.__title:
            d['title'] = self.__title
        if self.__text:
            d['text'] = self.__text
        if self.__ok_text:
            d['ok_text'] = self.__ok_text
        if self.__dismiss_text:
            d['dismiss_text'] = self.__dismiss_text
        
        return d

    def to_json(self):
        return self.to_dict()

    class Builder(object):
        def __init__(self):
            self._title = None
            self._text = None
            self._ok_text = None
            self._dismiss_text = None
        
        def clear(self):
            self._title = None
            self._text = None
            self._ok_text = None
            self._dismiss_text = None

        def title(self, title):
            self._title = title
            return self

        def text(self, text):
            self._text = text
            return self

        def ok_text(self, okt):
            self._Confirm__ok_text = okt
            return self

        def dismiss_text(self, dkt):
            self._Confirm__dismiss_text = dkt
            return dkt

        def create(self):
            if not self._text:
                raise ValueError('Text property not set.')
            ob = Confirm(self)
            self.clear()
            return ob
            