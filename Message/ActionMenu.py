from Action import Action
import json

class ActionMenu(Action):

    def __init__(self, builder):
        super(ActionMenu, self).__init__(builder)
        self.__type = builder._type
        self.__options = builder._options
        self.__option_groups = builder._option_groups
        self.__select_idx = builder._select_idx

    def to_dict(self):
        d = super(ActionMenu, self).to_dict()
        d['type'] = self.__type
        
        if len(self.__options) > 0:
            dd = []
            for opt in self.__options:
                dd.append(opt.to_dict())

            if self.__select_idx > 0 and self.__select_idx < len(self.__options):
                d[self.__select_idx], d[0] = d[0], d[self.__select_idx]
                d['selected_options'] = dd
            else:
                d['options'] = dd
        
        if len(self.__option_groups) > 0:
            dd = []
            for optg in self.__option_groups:
                dd.append(optg.to_dict())
            d['option_groups'] = dd
        
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(Action.Builder):
        def __init__(self):
            super(ActionMenu.Builder, self).__init__()
            self._type = 'select'
            self._options = []
            self._option_groups = [] # option groups replace options
            self._select_idx = -1

        def clear(self):
            super(ActionMenu.Builder, self).clear()
            self._type = 'select'
            self._options = []
            self._option_groups = [] # option groups replace options
            self._select_idx = -1       
              
        def name(self, name):
            super(ActionMenu.Builder, self).name(name)
            return self

        def text(self, text):
            super(ActionMenu.Builder, self).text(text)
            return self

        def value(self, value):
            super(ActionMenu.Builder, self).value(value)
            return self

        def confirm(self, cfm):
            super(ActionMenu.Builder, self).confirm(cfm)
            return self

        def selectOption(self, idx):
            self._select_idx = idx
            return self
        
        def addOption(self, opt):
            self._options.append(opt)
            return self

        def addOptionGroup(self, optg):
            self._option_groups.append(optg)
            return self 

        def create(self):
            ob = ActionMenu(self)
            self.clear()
            return ob
