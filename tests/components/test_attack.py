from src.core.objects import GameObject, MovementComponent
from src.scenes.main.objects import AttackComponent, HealthComponent

def test_attack():
    obj1 = GameObject()
    obj1.add(AttackComponent(obj1, "enemy", 50, 1))
    obj2 = GameObject()
    obj2.add(HealthComponent(obj2, 100))
    obj1.get(AttackComponent).handle_collision(obj2)
    assert obj2.get(HealthComponent).hp == 100
    obj2.tags.add("enemy")
    obj1.get(AttackComponent).handle_collision(obj2)
    assert obj2.get(HealthComponent).hp == 50