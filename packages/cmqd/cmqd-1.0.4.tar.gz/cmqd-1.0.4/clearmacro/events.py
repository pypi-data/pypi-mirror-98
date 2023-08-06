class Events:
    def __init__(self):
        self.events = {}

    def _on(self, event_name, handler):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(handler)
        handler_id = len(self.events[event_name]) - 1
        return handler_id

    def _off(self, event_name, handler):
        if event_name in self.events and handler in self.events[event_name]:
            self.events[event_name].remove(handler)
            return True
        return False

    def _emit(self, event_name, *args, **keywargs):
        if event_name in self.events:
            for handler in self.events[event_name]:
                handler(*args, **keywargs)
