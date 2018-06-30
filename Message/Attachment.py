import json
class Attachment(object):
    COLOR_GOOD = 'good'
    COLOR_WARN = 'warning'
    COLOR_DANGER = 'danger'
    
    def __init__(self, builder):
        self.__text = builder._text
        self.__title = builder._title
        self.__title_link = builder._title_link
        self.__fallback = builder._fallback
        self.__color = builder._color
        self.__callback_id = builder._callback_id
        self.__actions = builder._actions
        self.__fields = builder._fields
        builder.clear()


    def to_dict(self):
        d = {}
        if self.__title:
            d['title'] = self.__title
        if self.__title_link:
            d['title_link'] = self.__title_link
        if self.__text:
            d['text'] = self.__text
        if self.__fallback:
            d['fallback'] = self.__fallback
        if self.__color:
            d['color'] = self.__color
        if self.__callback_id:
            d['callback_id'] = self.__callback_id
        if len(self.__actions):
            dd = []
            for act in self.__actions:
                dd.append(act.to_dict())
            d['actions'] = dd
        if len(self.__fields):
            dd = []
            for fld in self.__fields:
                dd.append(fld.to_dict())
            d['fields'] = dd
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(object):
        def __init__(self):
            self._text = None
            self._title = None
            self._title_link = None
            self._fallback = None
            self._color = None
            self._callback_id = None
            self._actions = []
            self._fields = []
        
        def clear(self):
            self._text = None
            self._title = None
            self._title_link = None
            self._fallback = None
            self._color = None
            self._callback_id = None
            self._actions = []
            self._fields = []
            
        def title(self, title):
            self._title = title
            return self

        def title_link(self, link):
            self._title_link = link
            return self

        def text(self, txt):
            self._text = txt
            return self

        def fallback(self, fbk):
            self._fallback = fbk
            return self

        def color(self, clr):
            self._color = clr
            return self

        def callback_id(self, callback_id):
            self._callback_id = callback_id
            return self
        
        def addAction(self, action):
            self._actions.append(action)
            return self
        
        def addField(self, fld):
            self._fields.append(fld)
            return self

        def create(self):
            if not self._fallback:
                raise ValueError('fallback content must be set.')
            if not self._callback_id:
                raise ValueError('callback id must be set.')
            l = len(self._actions)
            return Attachment(self)