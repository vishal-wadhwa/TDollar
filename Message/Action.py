class Action(object):

    def __init__(self, builder):
        self.__name = builder._name
        self.__text = builder._text
        self.__value = builder._value
        self.__confirm = builder._confirm

    def to_dict(self):
        d = {}
        if self.__name:
            d['name'] = self.__name

        if self.__text:
            d['text'] = self.__text

        if self.__value:
            d['value'] = self.__value
        
        if self.__confirm:
            d['confirm'] = self.__confirm.to_dict()
        return d

    def to_json(self):
        raise NotImplementedError

    class Builder(object):
        def __init__(self):
            self._name = None
            self._text = None
            self._value = None
            self._confirm = None

        def clear(self):
            self._name = None
            self._text = None
            self._value = None
            self._confirm = None

        def name(self, name):
            self._name = name
            return self

        def text(self, text):
            self._text = text
            return self

        def value(self, value):
            self._value = value
            return self

        def confirm(self, cfm):
            self._confirm = cfm
            return self

        def create(self):
            if not self._name:
                raise ValueError('Must specify action name.')
            if not self._text:
                raise ValueError('Must specify action text.')
            ob = Action(self)
            self.clear()
            return ob
            
    

