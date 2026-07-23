import win32gui
import share
import subprocess
import os
import function
import pyautogui
import ctypes
import pydirectinput
from time import sleep
from function import load_path, save_path
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
    
    # 点击37并验证38，等待1s
    function.pic_operate_with_check_with_success_sleep(
        r"Nikke_img/37.png", r"Nikke_img/38.png", 1.0)  # 等待1秒
    # 点击38，这里需要等久一点,使用特殊函数，然后验证39
    function.nikke_spec1_pic_operate_with_check_with_success_sleep(
        r"Nikke_img/38.png", r"Nikke_img/39.png", 1.0)  # 等待1秒

    # 点击39并验证40，等待1s
    function.pic_operate_with_check_with_success_sleep(
        r"Nikke_img/39.png", r"Nikke_img/40.png", 1.0)  # 等待1秒
    # 点击40并验证37，等待1s
    function.pic_operate_with_check_with_success_sleep(
        r"Nikke_img/40.png", r"Nikke_img/37.png", 1.0)  # 等待1秒
    # 按下esc并验证24，等待0.5s
    function.press_key_with_check('esc', r"Nikke_img/24.png")
    sleep(0.5)
    # 点击24并验证25，等待1s
    function.pic_operate_with_check_with_success_sleep(
        r"Nikke_img/24.png", r"Nikke_img/25.png", 1.0)  # 等待1s
    # 点击25并验证41，等待1s
    function.pic_operate_with_check_with_success_sleep(
        r"Nikke_img/25.png", r"Nikke_img/41.png", 1.0)  # 等待1s
    # 点击绝对坐标1280，927，并验证25，等待1s
    function.click_abs_with_check(1280, 927, r"Nikke_img/25.png")
    sleep(1)
    # 点击25
    function








    # 你后续所有业务代码，全部写在这个函数里

# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    run_task()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    run_task()  # 同样调用复用
