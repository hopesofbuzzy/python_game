class ComponentRegistry:
    """
        Регистр компонентов для динамического
        добавления по названиям и полям.
    """

    _factories: dict[str, type] = dict()

    @classmethod
    def register(cls, name: str):
        """Регистрация компонента component_class (декоратор)."""

        def wrapper(component_class: type):
            cls._factories[name] = component_class
            return component_class

        return wrapper

    @classmethod
    def create(cls, name: str, entity, **kwargs):
        """Создание компонента по названию из регистра."""
        return cls._factories[name](entity, **kwargs)
