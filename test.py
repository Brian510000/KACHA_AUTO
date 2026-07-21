import win32con
import win32gui
import pydirectinput
import pyautogui
import ctypes
# from pyautogui import locateOnScreen, ImageNotFoundException, moveTo, click, moveRel, press
from time import sleep
from retry import retry
import function


# ========== 全局初始化（解决Windows缩放偏移） ==========
ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
pyautogui.PAUSE = 0.2  # 操作间隔，防操作过快

# ========== 配置项 ==========
IMG_CONFIDENCE = 0.8
RETRY_DELAY = 1
MAX_RETRY = 30  # 不建议无限重试
CHECK_MAX_TIMES = 10  # 验证图片最大重试次数
CHECK_INTERVAL = 1    # 验证图片查找间隔(秒)

# 【核心】把原有执行逻辑抽成独立函数，只写一次


def run_task():
    hwnd = function.get_target_window_hwnd("NIKKE")
    function.force_foreground_window(hwnd)
    win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
    # 你后续所有业务代码，全部写在这个函数里

# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    run_task()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    run_task()  # 同样调用复用
