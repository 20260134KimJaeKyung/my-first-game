
from entities.enemy import Enemy


class TankEnemy(Enemy):
    """느리지만 크고 튼튼한 적. 붉게 물들여 일반 적과 구분한다."""

    def __init__(self, x, y):

        super().__init__(
            x,
            y,
            size=72,
            speed=1.2,
            hp=12,
            xp_value=4,
            touch_damage=0.45,
            tint=(255, 120, 120),
        )
