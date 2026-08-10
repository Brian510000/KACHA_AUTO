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


    hwnd = function.get_target_window_hwnd("异环")

    function.force_foreground_window(hwnd)

# 点击32并验证33过一秒
    function.pic_operate_with_check(r"nte_img\43.png", r"nte_img\33.png")
    sleep(1)

    # 点击33并验证34过一秒
    function.pic_operate_with_check(r"nte_img\33.png", r"nte_img\34.png")
    sleep(1)

    # esc过一秒
    pydirectinput.press('esc')
    sleep(1)

    # esc过一秒并验证图片3
    function.press_key_with_check('esc', r"nte_img\3.png")
    sleep(1)
    # 点击35并验证36 过2秒
    function.pic_operate_with_check(r"nte_img\35.png", r"nte_img\36.png")
    sleep(2)

    # 点击910,318并验证2 过一秒
    function.click_abs_with_check(910, 318, r"nte_img\2.png")
    sleep(1)

    # 按下esc过一秒
    pydirectinput.press('esc')
    sleep(1)

    # 按下esc并验证 19或20其一 过一秒
    function.press_key_with_two_check(
        'esc', r"nte_img\19.png", r"nte_img\20.png")
    sleep(1)

    # 按下f2验证37过一秒
    function.press_key_with_check('f2', r"nte_img\37.png")
    sleep(1)

    # 点击38并验证35 过一秒
    function.pic_operate_with_check(r"nte_img\38.png", r"nte_img\35.png")
    sleep(1)

    # 点击39过1秒
    function.click_pic(r"nte_img\39.png")
    sleep(1)

    # 点击40验证41过一
    function.pic_operate_with_check(r"nte_img\40.png", r"nte_img\41.png")
    sleep(1)

    # 点击41过一
    function.click_pic(r"nte_img\41.png")
    sleep(1)

    # esc过一
    pydirectinput.press('esc')
    sleep(1)

    # esc验证19/20
    function.press_key_with_two_check(
        'esc', r"nte_img\19.png", r"nte_img\20.png")



    # 你后续所有业务代码，全部写在这个函数里

# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    run_task()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    run_task()  # 同样调用复用
