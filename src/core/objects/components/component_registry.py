class ComponentRegistry:
    _factories: dict[str, type] = dict()

    @classmethod
    def register(cls, name: str):
        def wrapper(component_class: type):
            cls._factories[name] = component_class
            return component_class
        return wrapper

    @classmethod
    def create(cls, name: str, entity, **kwargs):
        return cls._factories[name](entity, **kwargs)