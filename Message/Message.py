import json
class Message(object):
    IN_CHANNEL = 'in_channel'
    EPHEMERAL = 'ephemeral'
    def __init__(self, builder):
        self.__text = builder.txt
        self.__attachments = builder.attachments[:]
        self.__response_type = builder.res_type  
    
    def to_dict(self):
        d = {}
        if self.__text:
            d['text'] = self.__text
        if self.__response_type:
            d['response_type'] = self.__response_type
        if len(self.__attachments):
            dd = []
            for a in self.__attachments:
                dd.append(a.to_dict())
            d['attachments'] = dd
        return d
    
    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(object):
        def __init__(self):
            self.txt = None
            self.attachments = []
            self.res_type = None
        
        def clear(self):
            self.txt = None
            self.attachments = []
            self.res_type = None
            
        def text(self, msg):
            self.txt = msg
            return self

        def attach(self, attach_obj):
            self.attachments.append(attach_obj)
            return self

        def response_type(self, res_type):
            if res_type != Message.IN_CHANNEL or res_type != Message.EPHEMERAL:
                raise ValueError('response_type must be IN_CHANNEL or EPHEMERAL.')
            self.res_type = res_type
            return self

        def create(self):
            ob = Message(self)
            self.clear()
            return ob
    
