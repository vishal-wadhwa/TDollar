import json

class OptionGroup(object):

    def __init__(self, builder):
        self.__text = builder.txt
        self.__options = builder.options[:]
        builder.clear()        


    def to_dict(self):
        d = {}
        if self.__text:
            d['text'] = self.__text
        if len(self.__options) > 0:
            dd = []
            for op in self.__options:
                dd.append(op.to_dict())
            d['options'] = dd
        return d
    
    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(object):
        def __init__(self):
            self.txt = None
            self.options = []

        def clear(self):
            self.txt = None
            self.options = []
            
        def text(self, text):
            self.txt = text
            return self

        def addOption(self, opt):
            self.options.append(opt)
            return self

        def create(self):
            if not self.txt:
                raise ValueError('OptionGroup text must be set.')
            if len(self.options) == 0:
                raise ValueError('OptionGroup must have at least one option')
            return OptionGroup(self)
