#!/usr/bin/env python3
# 机器人 Hello World - 主程序
# 运行方式：python3 main.py
# 控制：方向键/WASD移动，空格扫描，M地图，R重置，Q/ESC退出

import sys
import io
import tty
import termios

# 修复 Windows 终端编码问题（WSL2/Linux 下不需要这行）
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── 第三方库 ──────────────────────────────────────────────
from colorama import init, Fore, Style
from art import text2art

# 初始化 colorama（Windows 兼容）
init()

from robot import Robot
from sensor import Sensor
from world import World


# ── 键盘输入（阻塞式，按下了才返回） ──────────────────────
KEY_UP    = "KEY_UP"
KEY_DOWN  = "KEY_DOWN"
KEY_LEFT  = "KEY_LEFT"
KEY_RIGHT = "KEY_RIGHT"
KEY_ESC   = "KEY_ESC"


def get_key():
    """阻塞式读取一个按键，没有输入时一直等待。
    返回值：
      普通字符 -> 原始字符如 'w', 'Q', ' '
      方向键   -> KEY_UP / KEY_DOWN / KEY_LEFT / KEY_RIGHT
      ESC     -> KEY_ESC
    """
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":          # ESC 序列开头（方向键）
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == "[":
                arrow_map = {"A": KEY_UP, "B": KEY_DOWN, "C": KEY_RIGHT, "D": KEY_LEFT}
                if ch3 in arrow_map:
                    return arrow_map[ch3]
            return KEY_ESC
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ── 绘制完整界面 ──────────────────────────────────────────
def draw_screen(world, robot):
    """一次性绘制地图 + HUD + 控制提示（替代 blessed 的清屏定位）"""
    print("\033[2J\033[H", end="")  # ANSI 清屏 + 光标归位
    world.display(robot)
    draw_hud(robot)
    draw_controls()


def draw_hud(robot):
    """绘制状态栏"""
    bar_len = 20
    filled = int(robot.battery / 100 * bar_len)
    bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"
    if robot.battery > 50:
        battery_color = Fore.GREEN
    elif robot.battery > 20:
        battery_color = Fore.YELLOW
    else:
        battery_color = Fore.RED

    print(f"  {Fore.CYAN}Pos: ({robot.x},{robot.y}){Style.RESET_ALL}  "
          f"{Fore.CYAN}Dir: {robot._direction_name()}{Style.RESET_ALL}  "
          f"{Fore.CYAN}Steps: {robot.steps}{Style.RESET_ALL}  "
          f"{Fore.GREEN}Treasures: {len(robot.collected)}{Style.RESET_ALL}")
    print(f"  Battery {battery_color}{bar}{Style.RESET_ALL} {robot.battery:.0f}%")


def battery_bar(battery):
    """生成简短的电量条字符串（含颜色）"""
    bar_len = 12
    filled = int(battery / 100 * bar_len)
    bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"
    if battery > 50:
        c = Fore.GREEN
    elif battery > 20:
        c = Fore.YELLOW
    else:
        c = Fore.RED
    return f"{c}{bar}{Style.RESET_ALL} {battery:.0f}%"


def draw_controls():
    """绘制操控提示"""
    print(f"  {Style.BRIGHT}Controls:{Style.RESET_ALL}  "
          f"{Fore.YELLOW}[Arrow/WASD]{Style.RESET_ALL} Move  "
          f"{Fore.YELLOW}[SPACE]{Style.RESET_ALL} Scan  "
          f"{Fore.YELLOW}[M]{Style.RESET_ALL} Map  "
          f"{Fore.YELLOW}[R]{Style.RESET_ALL} Reset  "
          f"{Fore.YELLOW}[Q]{Style.RESET_ALL} Quit")


# ── 欢迎界面 ──────────────────────────────────────────────
def print_welcome():
    """绘制欢迎界面（含 ASCII Art 标题）"""
    title = text2art("ROBOT", font="block")
    print()
    print(f"  {Fore.CYAN}{Style.BRIGHT}{'=' * 46}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}{Style.BRIGHT}   Robot Hello World - Your First Robot!{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}{'=' * 46}{Style.RESET_ALL}")
    for line in title.strip().split('\n'):
        print(f"    {Fore.GREEN}{line}{Style.RESET_ALL}")
    print()
    print(f"  {Style.DIM}  Use ARROW KEYS or WASD to move the robot{Style.RESET_ALL}")
    print(f"  {Style.DIM}  Collect all treasures (*) and reach the goal (G)!{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}{'=' * 46}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}  Press any key to start...{Style.RESET_ALL}")
    print()
    get_key()  # 阻塞等待，按任意键开始


# ── 胜利画面 ──────────────────────────────────────────────
def draw_victory(robot, world):
    """显示胜利结束画面"""
    total_treasures = sum(row.count("*") for row in world.map) + len(robot.collected)
    print("\033[2J\033[H", end="")  # 清屏

    # ── 大号 ASCII Art 标题（用 art 库生成） ──
    title_art = text2art("YOU WIN", font="block")
    art_lines = title_art.strip().split('\n')

    print()
    # 计算居中
    max_len = max(len(line) for line in art_lines)
    for line in art_lines:
        pad = (max_len - len(line)) // 2
        print(f"    {Fore.YELLOW}{Style.BRIGHT}{' ' * max(pad, 0)}{line}{Style.RESET_ALL}")

    # ── 分隔线 ──
    W = 46
    print(f"\n  {Fore.GREEN}{Style.BRIGHT}{'=' * W}{Style.RESET_ALL}")

    # ── 战绩面板 ──
    stat_rows = [
        ("Robot Name", f"{Style.BRIGHT}{robot.name}{Style.RESET_ALL}"),
        ("Total Steps", f"{Style.BRIGHT}{robot.steps}{Style.RESET_ALL}"),
        ("Treasures", f"{Fore.YELLOW}{Style.BRIGHT}{len(robot.collected)} / {total_treasures}{Style.RESET_ALL}"),
        ("Battery Left", battery_bar(robot.battery)),
    ]
    for label, value in stat_rows:
        print(f"    {Fore.CYAN}{label:<14}{Style.RESET_ALL}: {value}")

    print(f"  {Fore.GREEN}{Style.BRIGHT}{'=' * W}{Style.RESET_ALL}")

    # ── 评级 ──
    score = len(robot.collected) / max(total_treasures, 1)
    if score == 1:
        grade, color, comment = "S", Fore.YELLOW, "PERFECT  -  All treasures collected!"
    elif score >= 0.6:
        grade, color, comment = "A", Fore.GREEN, "EXCELLENT  -  Most treasures found!"
    elif score >= 0.3:
        grade, color, comment = "B", Fore.CYAN, "GOOD JOB  -  Room to improve."
    else:
        grade, color, comment = "C", Fore.WHITE, "COMPLETED  -  Try again for more!"

    print(f"    {Fore.CYAN}GRADE{Style.RESET_ALL}: "
          f"[{color}{Style.BRIGHT} {grade} {Style.RESET_ALL}]  {comment}")
    print(f"  {Fore.GREEN}{Style.BRIGHT}{'=' * W}{Style.RESET_ALL}")

    # ── 结束语 ──
    print()
    print(f"  {Fore.GREEN}{Style.BRIGHT}  Congratulations! You completed the maze!{Style.RESET_ALL}")
    print(f"  {Style.DIM}  This is what running a robot program feels like.{Style.RESET_ALL}")
    print()
    print(f"    {Fore.YELLOW}  >> Press any key to exit <<{Style.RESET_ALL}")
    print()
    get_key()


# ── 移动逻辑 ──────────────────────────────────────────────
def try_move(robot, world, direction):
    """尝试朝指定方向移动一步，返回是否成功"""
    robot.direction = direction
    old_x, old_y = robot.x, robot.y
    robot.walk(1)
    if not world.can_move(robot.x, robot.y):
        robot.x, robot.y = old_x, old_y
        print(f"  {Fore.RED}[!] Wall ahead! Can not move.{Style.RESET_ALL}")
        return False
    return True


# ── 主程序 ────────────────────────────────────────────────
def main():
    print_welcome()

    # 创建机器人、传感器和世界
    robot = Robot("Robo")
    robot.x, robot.y = 1, 1  # 起始位置 (1,1)，避免卡在墙角
    robot.silent = True
    sensor = Sensor(robot)
    world = World()
    game_over = False

    # 绘制初始界面
    draw_screen(world, robot)
    print(f"\n  {Fore.GREEN}> {Style.RESET_ALL}", end="", flush=True)

    # 主循环 —— 只有按键才触发
    while not game_over:
        key = get_key()  # 阻塞等待按键

        moved = False

        # ── 方向键移动 ──
        if key == KEY_UP:
            moved = try_move(robot, world, 0)
        elif key == KEY_DOWN:
            moved = try_move(robot, world, 180)
        elif key == KEY_LEFT:
            moved = try_move(robot, world, 270)
        elif key == KEY_RIGHT:
            moved = try_move(robot, world, 90)

        # ── WASD 备用控制 ──
        elif key in ("w", "W"):
            moved = try_move(robot, world, 0)
        elif key in ("s", "S"):
            moved = try_move(robot, world, 180)
        elif key in ("a", "A"):
            moved = try_move(robot, world, 270)
        elif key in ("d", "D"):
            moved = try_move(robot, world, 90)

        # ── 功能键 ──
        elif key == " ":              # 空格 = 扫描（在当前画面下方追加扫描结果）
            sensor.scan(world)
            print(f"  {Fore.GREEN}> {Style.RESET_ALL}", end="", flush=True)
            continue  # 不重绘地图，让扫描信息停留

        elif key in ("m", "M"):       # M = 重新绘制地图
            draw_screen(world, robot)
            print(f"\n  {Fore.GREEN}> {Style.RESET_ALL}", end="", flush=True)
            continue

        elif key in ("r", "R"):       # R = 重置
            robot.x, robot.y = 1, 1
            robot.direction = 0
            robot.battery = 100
            robot.steps = 0
            robot.collected = []
            world = World()
            draw_screen(world, robot)
            print(f"\n  {Fore.GREEN}[OK] Game reset!{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}> {Style.RESET_ALL}", end="", flush=True)
            continue

        elif key == KEY_ESC or key in ("q", "Q"):  # Q / ESC = 退出
            print(f"\n  {Fore.CYAN}{robot.name} powering off. Bye!{Style.RESET_ALL}\n")
            game_over = True
            continue

        # 移动后：检查事件 → 重绘界面
        if moved:
            event = world.try_collect(robot)
            if event == "goal":
                # 到达终点 → 显示胜利画面
                draw_victory(robot, world)
                game_over = True
            else:
                # 宝箱已由 try_collect 打印提示，直接重绘
                draw_screen(world, robot)
                print(f"\n  {Fore.GREEN}> {Style.RESET_ALL}", end="", flush=True)


if __name__ == "__main__":
    main()
