# 机器人基础类 —— 机器人的"身体"
# 这个文件定义了机器人有哪些能力和状态

class Robot:
    """一个小型移动机器人"""

    def __init__(self, name="Robo"):
        self.name = name
        # 位置：用 (x, y) 坐标表示
        self.x = 0
        self.y = 0
        # 方向：0=北(上), 90=东(右), 180=南(下), 270=西(左)
        self.direction = 0  # 初始朝北
        # 电池电量
        self.battery = 100
        # 行走步数统计
        self.steps = 0
        # 已收集的宝箱
        self.collected = []
        # 静默模式：键盘控制时不打印每次移动信息
        self.silent = False

    def _say(self, msg):
        """根据静默模式决定是否打印信息"""
        if not self.silent:
            print(msg)

    def walk(self, steps=1):
        """向前走指定步数"""
        for _ in range(steps):
            if self.battery <= 0:
                self._say(f"  [!] {self.name} is out of battery! Use 'charge' to recharge.")
                return
            # 根据当前方向移动
            if self.direction == 0:     # 北
                self.y += 1
            elif self.direction == 90:  # 东
                self.x += 1
            elif self.direction == 180: # 南
                self.y -= 1
            elif self.direction == 270: # 西
                self.x -= 1
            self.battery -= 0.5
            self.steps += 1
        self._say(f"  >> {self.name} walked {steps} step(s) toward {self._direction_name()}")

    def back(self, steps=1):
        """向后退指定步数"""
        for _ in range(steps):
            if self.battery <= 0:
                self._say(f"  [!] {self.name} is out of battery!")
                return
            if self.direction == 0:
                self.y -= 1
            elif self.direction == 90:
                self.x -= 1
            elif self.direction == 180:
                self.y += 1
            elif self.direction == 270:
                self.x += 1
            self.battery -= 0.5
            self.steps += 1
        self._say(f"  >> {self.name} backed {steps} step(s) from {self._direction_name()}")

    def turn_left(self, degrees=90):
        """向左转（逆时针）"""
        self.direction = (self.direction - degrees) % 360
        self._say(f"  >> {self.name} turned left {degrees} deg, now facing {self._direction_name()}")

    def turn_right(self, degrees=90):
        """向右转（顺时针）"""
        self.direction = (self.direction + degrees) % 360
        self._say(f"  >> {self.name} turned right {degrees} deg, now facing {self._direction_name()}")

    def status(self):
        """显示机器人当前状态"""
        print(f"\n  +-- {self.name}'s Status Report ----------+")
        print(f"  |  Position : ({self.x}, {self.y})")
        print(f"  |  Facing   : {self._direction_name()} ({self.direction} deg)")
        print(f"  |  Battery  : {self.battery:.1f}%")
        print(f"  |  Steps    : {self.steps}")
        print(f"  |  Treasures: {len(self.collected)} {self.collected}")
        print(f"  +------------------------------------+")

    def charge(self):
        """充电"""
        self.battery = 100
        self._say(f"  [OK] {self.name} fully charged! Battery: 100%")

    def _direction_name(self):
        """将角度转换为方向名称"""
        names = {0: "NORTH", 90: "EAST", 180: "SOUTH", 270: "WEST"}
        closest = min(names.keys(), key=lambda k: abs(k - self.direction))
        if abs(closest - self.direction) <= 45:
            return names[closest]
        return f"{self.direction} deg"
