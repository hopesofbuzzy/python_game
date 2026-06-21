import logging
import weakref
from dataclasses import dataclass
from typing import Callable


@dataclass
class Listener:
    listener: Callable
    priority: int
    is_alive: bool = True

@dataclass
class EventFlow:
    is_stopped: bool = False

    def stop(self):
        self.is_stopped = True

class EventBus:
    """
        Глобальная шина событий с системой приоритетов.
        Используется для приоритезации ввода и
        для глобальных событий, интересных основной сцене или многим
        объектам.

        Больше приоритет -> первее получает событие.
    """
    def __init__(self):
        self.listeners: dict[str, list[Listener]] = dict()

    def subscribe(self, event_name, listener, priority=None):
        """
            Подписка слушателя на событие.
        
            event_name: название события.
            listener: функция-слушатель.
            priority: приоритет слушателя (выше приоритет -> первее получение).
        """
        if not priority:
            priority = -1
        self.listeners[event_name] = self.listeners.get(event_name, [])
        # Храним слабую ссылку, чтобы не было УТЕЧЕК ПАМЯТИ!
        if hasattr(listener, "__self__"):
            self.listeners[event_name].append(
                Listener(weakref.WeakMethod(listener), priority)
            )
        else:
            self.listeners[event_name].append(Listener(listener, priority))
        # Сортировка по приоритету
        self.listeners[event_name] = sorted(
            self.listeners[event_name], key=lambda x: x.priority, reverse=True
        )

    def fire(self, event_name, *args):
        """
            Вызов события и оповещение слушателей.

            Args:
                event_name: название события.
        """
        self.listeners[event_name] = self.listeners.get(event_name, [])
        for listener in self.listeners[event_name]:
            event = EventFlow()
            if isinstance(listener.listener, weakref.WeakMethod):
                alive_func = listener.listener()
                if not alive_func:
                    listener.is_alive = False
                    continue
                alive_func(event, *args)
                if event.is_stopped:
                    break
            else:
                listener.listener(event, *args)
            if event.is_stopped:
                break
        # Пересоздаём список вызова для O(n)
        self.listeners[event_name] = [
            l
            for l in self.listeners[event_name]
            if l.is_alive
        ]

# Глобальная шина.
event_bus = EventBus()