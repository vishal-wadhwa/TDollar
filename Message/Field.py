import json

class Field(object):
    def __init__(self, builder):
        self.__title = builder.titl
        self.__value = builder.val
        self.__short = builder.shorty

    def to_dict(self):
        d = {}
        if self.__title:
            d['title'] = self.__title
        if self.__value:
            d['value'] = self.__value
        d['short'] = self.__short
        return d
    
    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(object):
        def __init__(self):
            self.titl = None
            self.val = None
            self.shorty = False

        def clear(self):
            self.titl = None
            self.val = None
            self.shorty = False
        
        def title(self, title):
            self.titl = title
            return self
        
        def value(self, value):
            self.val = value
            return self
        
        def short(self, short):
            self.shorty = short            
        
        def create(self):
            if not self.val:
                raise ValueError('Field value must be set.')
            if not self.titl:
                raise ValueError('Field title must be set.')
            ob = Field(self)
            self.clear()
            return ob