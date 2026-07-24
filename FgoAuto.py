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
CHECK_MAX_TIMES = 15  # 验证图片最大重试次数
CHECK_INTERVAL = 1    # 验证图片查找间隔(秒)

# 启动程序（异步，不等待退出）


def launch_game(config_key, game_name):
    path = load_path(config_key)
    print(f"读取到的路径：{repr(path)}")          # 显示原始字符串
    print(f"是否为文件：{os.path.isfile(path)}")  # 判断是否为文件
    print(f"是否存在：{os.path.exists(path)}")    # 是否存在
    if not path:
        print("路径为空")
        return
    if not os.path.exists(path):
        print("路径不存在")
        return
    if not os.path.isfile(path):
        print("路径不是文件（可能是目录），请检查")
        return

    subprocess.Popen([path, "-v", "1"])
    print(f"已启动：{path}")

def fgo():
    launch_game("fgo", "FGO")

    hwnd = function.get_target_window_hwnd("安卓设备")


    function.force_foreground_window(hwnd)

    sleep(10)

    if function.check_pic_exist_in_times(r"fgo_img\1.png", 7, hwnd):
        function.window_click_pic(r"fgo_img\1.png", hwnd)

    sleep(1)

    function.window_pic_operate_with_check(
        r"fgo_img\5.png", r"fgo_img\6.png", hwnd)
    sleep(15)
    function.window_pic_operate_with_check(
        r"fgo_img\6.png", r"fgo_img\6_1.png", hwnd)
    sleep(1)
    function.window_pic_operate_with_check(
        r"fgo_img\6_1.png", r"fgo_img\6_2.png", hwnd)
    sleep(1)
    function.window_pic_operate_with_check(
        r"fgo_img\6_2.png", r"fgo_img\6_3.png", hwnd)
    sleep(1)
    function.window_pic_operate_with_check(
        r"fgo_img\6_3.png", r"fgo_img\6_4.png", hwnd)
    sleep(1)
    function.window_pic_operate_with_check(
        r"fgo_img\6_4.png", r"fgo_img\6_5.png", hwnd)
    sleep(1)
    # 点击0并验证5，过一秒
    function.window_pic_operate_with_check(
        r"fgo_img\0.png", r"fgo_img\5.png", hwnd)

    # 点击2，并且验证3，过2秒
    function.window_pic_operate_with_check(
        r"fgo_img\2.png", r"fgo_img\3.png", hwnd)
    sleep(2)

    # 点击3，并且验证4，过2秒
    function.window_pic_operate_with_check(
        r"fgo_img\3.png", r"fgo_img\4.png", hwnd)
    sleep(2)
    # 点击4，过3秒
    function.window_click_pic(r"fgo_img\4.png", hwnd)
    sleep(4)

    # 点击0并验证5，过一秒
    function.window_pic_operate_with_check(
        r"fgo_img\0.png", r"fgo_img\5.png", hwnd)

    # 点击8过10秒
    function.window_click_pic(r"fgo_img\8.png", hwnd)
    sleep(8)

    function.window_pic_operate_with_check(
        r"fgo_img\9.png", r"fgo_img\10.png", hwnd)


    sleep(2)

    # 点击10
    function.window_click_pic(r"fgo_img\10.png", hwnd)

    sleep(20)
    # 一直寻找并点击11（可能有很多个）
    while function.check_pic_exist_in_times(r"fgo_img\11.png", 3, hwnd):
        function.window_click_pic(r"fgo_img\11.png", hwnd)
        sleep(1)

    # 点击13并验证14
    function.window_pic_operate_with_check(
        r"fgo_img\13.png", r"fgo_img\14.png", hwnd)

    # 点击14并验证15，过一秒
    function.window_pic_operate_with_check(
        r"fgo_img\14.png", r"fgo_img\15.png", hwnd)
    sleep(1)
    # 点击15并验证16，过一秒
    function.window_pic_operate_with_check(
        r"fgo_img\15.png", r"fgo_img\16.png", hwnd)
    sleep(1)
    # 点击17，过一秒
    function.window_click_pic(r"fgo_img\17.png", hwnd)
    sleep(1)
    if function.check_pic_exist_in_times(r"fgo_img\18.png", 1, hwnd):
        function.window_click_pic(r"fgo_img\18.png", hwnd)
    # 点击19
    function.window_click_pic(r"fgo_img\19.png", hwnd)


# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    fgo()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    fgo()  # 同样调用复用
