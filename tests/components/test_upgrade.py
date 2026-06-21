from src.core.objects import GameObject, MovementComponent
from src.scenes.main.objects import UpgradeComponent
from src.core.singletones.event_bus import EventBus

def test_upgrade():
    obj1 = GameObject()
    event_bus = EventBus()
    obj1.add(UpgradeComponent(obj1, "target_plant", 100, event_bus))
    var = 0
    def plant_level_up(event, plant, target_plant):
        nonlocal var
        var += 1
        assert target_plant == "target_plant"
        assert plant is obj1
    event_bus.subscribe(
        "on_plant_level_uped",
        plant_level_up
    )
    obj1.get(UpgradeComponent).upgrade()
    assert var == 1