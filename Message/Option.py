import json

class Option(object):

    def __init__(self, builder):
        self.__text = builder.txt
        self.__value = builder.val
        self.__descr = builder.descr
        builder.clear()


    def to_dict(self):
        d = {}
        if self.__text:
            d['text'] = self.__text
        if self.__value:
            d['value'] = self.__value
        if self.__descr:
            d['description'] = self.__descr
        return d
    
    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(object):
        def __init__(self):
            self.txt = None
            self.val = None
            self.descr = None

        def clear(self):
            self.txt = None
            self.val = None
            self.descr = None

        def text(self, text):
            self.txt = text
            return self
        
        def value(self, value):
            self.val = value
            return self

        def descript(self, descr):
            self.descr = descr
            return self

        def create(self):
            if not self.txt:
                raise ValueError('Option text must be set.')
            if not self.val:
                raise ValueError('Option value must be set.')
            return Option(self)
