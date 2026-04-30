class Event:
    def __init__(self):
        self.listeners: list = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        self.listeners.remove(listener)

    def emit(self, *args):
        for listener in self.listeners:
            listener(*args)
