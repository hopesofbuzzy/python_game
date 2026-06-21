import weakref


class Event:
    """локальное событие (observer pattern)."""

    def __init__(self):
        self.listeners: list = []

    def subscribe(self, listener):
        """Подписка слушателя (listener) на событие."""
        # Храним слабую ссылку, чтобы не было УТЕЧЕК ПАМЯТИ!
        if hasattr(listener, "__self__"):
            self.listeners.append(weakref.WeakMethod(listener))
        else:
            self.listeners.append(listener)

    def unsubscribe(self, listener):
        """Отписка слушателя (listener) от события."""
        for listener_shell in self.listeners[:]:
            if isinstance(listener_shell, weakref.WeakMethod):
                alive_func = listener_shell()
                if alive_func == listener:
                    self.listeners.remove(listener_shell)
                    return
        self.listeners.remove(listener)

    def emit(self, *args):
        """Вызов события и оповещение слушателей."""
        dead_refs = list()
        for listener in self.listeners[:]:
            if isinstance(listener, weakref.WeakMethod):
                alive_func = listener()
                if not alive_func:
                    dead_refs.append(listener)
                    continue
                alive_func(*args)
            else:
                listener(*args)
        for dead_ref in dead_refs:
            self.listeners.remove(dead_ref)
