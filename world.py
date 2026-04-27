# 世界/地图 —— 机器人活动的场景
# 这个文件定义了机器人所在的环境和地图

from colorama import Fore, Style


class World:
    """机器人的活动世界"""

    def __init__(self):
        self.width = 15   # 地图宽度
        self.height = 10  # 地图高度
        # 用二维列表表示地图
        # "." = 空地, "#" = 墙壁, "*" = 宝箱, "G" = 终点(Goal)
        self.map = [
            list("###############"),
            list("#.............#"),
            list("#.*..#........#"),
            list("#....#..*..#..#"),
            list("#..#.....#.#..#"),
            list("#..#..*..#....#"),
            list("#....#...#..*.#"),
            list("#..#.....#....#"),
            list("#........*..G.#"),
            list("###############"),
        ]

    def get_cell(self, x, y):
        """获取指定位置的地图内容"""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.map[y][x]
        return "#"  # 超出地图范围视为墙壁

    def set_cell(self, x, y, value):
        """设置指定位置的地图内容"""
        if 0 <= y < self.height and 0 <= x < self.width:
            self.map[y][x] = value

    def can_move(self, x, y):
        """检查机器人能否移动到指定位置"""
        cell = self.get_cell(x, y)
        return cell != "#"

    def try_collect(self, robot):
        """检查当前位置是否有宝箱可以收集，或是否到达终点。
        返回: 'treasure' = 收集了宝箱, 'goal' = 到达终点, None = 无事件"""
        cell = self.get_cell(robot.x, robot.y)
        if cell == "*":
            self.set_cell(robot.x, robot.y, ".")
            robot.collected.append(f"({robot.x},{robot.y})")
            print(f"  {Fore.YELLOW}[*] {robot.name} picked up a treasure at ({robot.x}, {robot.y})!{Style.RESET_ALL}")
            print(f"     {Fore.GREEN}Treasures collected: {len(robot.collected)}{Style.RESET_ALL}")
            return "treasure"
        if cell == "G":
            return "goal"
        return None

    def display(self, robot):
        """在终端中绘制地图（带颜色）"""
        print(f"\n  {Fore.CYAN}[MAP] Robot World  ({self.width}x{self.height}){Style.RESET_ALL}")
        print("  +" + "-" * (self.width * 2 + 1) + "+")
        for y in range(self.height - 1, -1, -1):
            row = "  | "
            for x in range(self.width):
                if x == robot.x and y == robot.y:
                    # 绘制机器人，用箭头表示方向
                    arrows = {0: "^", 90: ">", 180: "v", 270: "<"}
                    arrow = arrows.get(robot.direction, "o")
                    row += f"{Fore.CYAN}{Style.BRIGHT}{arrow}{Style.RESET_ALL} "
                else:
                    cell = self.map[y][x]
                    if cell == ".":
                        row += "  "  # 空地
                    elif cell == "*":
                        row += f"{Fore.YELLOW}*{Style.RESET_ALL} "  # 宝箱（黄色）
                    elif cell == "G":
                        row += f"{Fore.GREEN}{Style.BRIGHT}G{Style.RESET_ALL} "  # 终点（绿色高亮）
                    else:
                        row += f"{Fore.BLUE}#{Style.RESET_ALL} "  # 墙壁（蓝色）
            row += "|"
            print(row)
        print("  +" + "-" * (self.width * 2 + 1) + "+")
        print(f"   {Fore.CYAN}^>v<{Style.RESET_ALL} = Robot   "
              f"{Fore.YELLOW}*{Style.RESET_ALL} = Treasure   "
              f"{Fore.GREEN}G{Style.RESET_ALL} = Goal   "
              f"{Fore.BLUE}#{Style.RESET_ALL} = Wall")
