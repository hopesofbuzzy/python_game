import weakref
import logging

class EventBus:
    def __init__(self):
        self.listeners: dict[str, list] = dict()

    def subscribe(self, event_name, listener):
        self.listeners[event_name] = self.listeners.get(event_name, [])
        # Храним слабую ссылку, чтобы не было УТЕЧЕК ПАМЯТИ!
        if hasattr(listener, "__self__"):
            self.listeners[event_name].append(weakref.WeakMethod(listener))
        else:
            self.listeners[event_name].append(listener)

    def fire(self, event_name, *args):
        logging.debug(event_name)
        dead_refs = list()
        self.listeners[event_name] = self.listeners.get(event_name, [])
        for listener in self.listeners.get(event_name, []):
            if isinstance(listener, weakref.WeakMethod):
                alive_func = listener()
                if not alive_func:
                    dead_refs.append(listener)
                    continue
                alive_func(*args)
            else:
                listener(*args)
        for dead_ref in dead_refs:
            self.listeners[event_name].remove(dead_ref)

event_bus = EventBus()