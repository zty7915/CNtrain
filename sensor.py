# 传感器类 —— 机器人的"感官"
# 这个文件定义了机器人如何感知周围环境

import random
from colorama import Fore, Style


class Sensor:
    """机器人的传感器系统"""

    def __init__(self, robot):
        self.robot = robot
        # 传感器探测距离（格数）
        self.range = 3

    def scan(self, world):
        """扫描周围环境，返回探测结果"""
        results = []
        # 四个方向都扫描
        directions = {
            "Front": 0,
            "Right": 90,
            "Back": 180,
            "Left": 270,
        }
        # 计算传感器实际朝向
        for label, offset in directions.items():
            check_dir = (self.robot.direction + offset) % 360
            # 在这个方向上逐格探测
            found = None
            for dist in range(1, self.range + 1):
                check_x = self.robot.x
                check_y = self.robot.y
                if check_dir == 0:
                    check_y += dist
                elif check_dir == 90:
                    check_x += dist
                elif check_dir == 180:
                    check_y -= dist
                elif check_dir == 270:
                    check_x -= dist
                # 检查这个位置有什么
                cell = world.get_cell(check_x, check_y)
                if cell == "#":
                    found = f"{label}: Wall at {dist} cell(s)"
                    break
                elif cell == "*":
                    found = f"{label}: Treasure at {dist} cell(s)"
                    break
            if found:
                results.append(found)

        # 显示扫描结果
        print(f"\n  {Fore.CYAN}>> {self.robot.name}'s Sensor Scan:{Style.RESET_ALL}")
        if results:
            for r in results:
                print(f"     |  {Fore.YELLOW}{r}{Style.RESET_ALL}")
        else:
            print(f"     +-- {Fore.GREEN}All clear! No obstacles detected.{Style.RESET_ALL}")

        # 也显示附近有没有宝箱可以捡
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                cell = world.get_cell(self.robot.x + dx, self.robot.y + dy)
                if cell == "*":
                    print(f"     +-- {Fore.YELLOW}Treasure nearby at ({self.robot.x + dx}, {self.robot.y + dy})! Walk toward it!{Style.RESET_ALL}")

        # 模拟传感器噪声（教学用，增加趣味性）
        noise = random.choice(["Sensor OK", "Signal stable", "All systems nominal"])
        print(f"     +-- {Fore.GREEN}[System] {noise}{Style.RESET_ALL}")

        return results
