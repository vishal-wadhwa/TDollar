from Action import Action
import json

class ActionButton(Action):
    STYLE_DANGER = 'danger'
    STYLE_DEFAULT = 'default'
    STYLE_PRIMARY = 'primary'

    def __init__(self, builder):
        super(ActionButton, self).__init__(builder)
        self.__type = builder._type
        self.__style = builder._style

    def to_dict(self):
        d = super(ActionButton, self).to_dict()
        d['type'] = self.__type
        d['style'] = self.__style
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    class Builder(Action.Builder):
        def __init__(self):
            super(ActionButton.Builder, self).__init__()
            self._type = 'button'
            self._style = ActionButton.STYLE_DEFAULT

        def clear(self):
            super(ActionButton.Builder, self).clear()
            self._type = 'button'
            self._style = ActionButton.STYLE_DEFAULT

        def name(self, name):
            super(ActionButton.Builder, self).name(name)
            return self

        def text(self, text):
            super(ActionButton.Builder, self).text(text)
            return self

        def value(self, value):
            super(ActionButton.Builder, self).value(value)
            return self

        def confirm(self, cfm):
            super(ActionButton.Builder, self).confirm(cfm)
            return self

        def style(self, style):
            if type != ActionButton.STYLE_DANGER or ActionButton.STYLE_DEFAULT \
                or ActionButton.STYLE_DANGER:
                raise ValueError('Incorrect style selected: ', style)
            self._style = style
            return self

        def create(self):
            ob = ActionButton(self)
            self.clear()
            return ob
