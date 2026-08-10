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
CHECK_MAX_TIMES = 5  # 验证图片最大重试次数
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

    subprocess.Popen([path])
    print(f"已启动：{path}")

def nte():

    launch_game("yihuan", "异环")
    # 如果希望等待程序运行结束再继续，使用 subprocess.run()
    # subprocess.run(nte_address)   # 会阻塞直到程序关闭

    function.click_pic(r"nte_img\image.png")

    sleep(50)

    hwnd = function.get_target_window_hwnd("异环")


    function.force_foreground_window(hwnd)


    function.pic_click_abs_with_check(r"nte_img\42.png", 1270, 1240, r"nte_img\imagecopy2.png")

    sleep(5)

    # '''
    # 点击图片1 验证 2
    function.pic_operate_with_check(r"nte_img\1.png", r"nte_img\2.png")
    # 过一秒按下esc,过两秒
    sleep(1)
    pydirectinput.press('esc')
    sleep(2)
    # '''
    # 按下b验证5 过一秒
    function.press_key_with_check('b', r"nte_img\5.png")
    sleep(1)
    # 点击6 过一秒
    function.click_pic(r"nte_img\6.png")
    # 点击7 验证8 过一秒
    function.pic_operate_with_check(r"nte_img\7.png", r"nte_img\8.png")
    sleep(1)

    # 点击8 过一秒
    function.click_pic(r"nte_img\8.png")
    sleep(1)

    # 如果是10则点击10 ,不是就不点,然后过一秒
    if function.check_pic_exist(r"nte_img\10.png"):
        function.click_pic(r"nte_img\10.png")

    # 点击11并验证12 过一秒
    function.pic_operate_with_check(r"nte_img\11.png", r"nte_img\12.png")
    sleep(1)

    # 点击14 过一秒
    function.click_pic(r"nte_img\14.png")
    sleep(1)
    # 点击15并且验证16 过一秒
    function.pic_operate_with_check(r"nte_img\15.png", r"nte_img\16.png")
    sleep(1)

    # 点击16 过0.5
    function.click_pic(r"nte_img\16.png")
    sleep(0.5)

    # 点击17 过二秒
    function.click_pic(r"nte_img\17.png")
    sleep(2)

    # 点击18 过一秒
    function.click_pic(r"nte_img\18.png")
    sleep(1)

    # 按一下esc
    pydirectinput.press('esc')
    sleep(1)
    # 按一下esc
    pydirectinput.press('esc')
    sleep(1)
    # 按一下esc
    pydirectinput.press('esc')
    sleep(1)
    # 按一下esc 并验证21
    function.press_key_with_check('esc', r"nte_img\21.png")
    sleep(1)
    # 点击坐标2077,1000 并验证 22 过一秒
    function.click_abs_with_check(2077, 1000, r"nte_img\22.png")
    sleep(1)

    # 点击22并验证23 过一秒
    function.pic_operate_with_check(r"nte_img\22.png", r"nte_img\23.png")
    sleep(1)
    # 点击23
    function.click_pic(r"nte_img\23.png")
    sleep(1)
    # 点击24 并验证26 过一秒
    function.pic_operate_with_check(r"nte_img\24.png", r"nte_img\26.png")
    sleep(1)

    # 按一下esc并验证21 过一.5秒
    function.press_key_with_check('esc', r"nte_img\21.png")
    sleep(1.5)

    # 点击坐标1920,618 并验证 27 过一秒
    function.click_abs_with_check(1920, 618, r"nte_img\27.png")
    sleep(1)

    # 点击28并验证29 过一秒
    function.pic_operate_with_check(r"nte_img\28.png", r"nte_img\29.png")
    sleep(1)

    # 点击650,618并验证30 过一秒
    function.click_abs_with_check(650, 618, r"nte_img\30.png")
    sleep(1)

    # 点击30 过1.5秒
    function.click_pic(r"nte_img\a1.png")
    sleep(1.5)

    # 按下esc
    pydirectinput.press('esc')
    sleep(1)

    # 按下esc
    pydirectinput.press('esc')
    sleep(1)

    # 按下esc并验证 19或者20其一
    function.press_key_with_two_check('esc', r"nte_img\19.png", r"nte_img\20.png")
    sleep(1)

    # 按下f1并验证3 过一秒
    function.press_key_with_check('f1', r"nte_img\3.png")
    sleep(1)

    # 按下图片4 过2秒
    function.click_pic(r"nte_img\4.png")
    sleep(2)

    # 点击32的绝对坐标2230，1104并验证33过一秒
    function.click_abs_with_check(2230,1104, r"nte_img\33.png")
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
    function.press_key_with_two_check('esc', r"nte_img\19.png", r"nte_img\20.png")
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
    function.press_key_with_two_check('esc', r"nte_img\19.png", r"nte_img\20.png")


# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    nte()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    nte()  # 同样调用复用
