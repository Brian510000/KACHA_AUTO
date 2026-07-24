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

    subprocess.Popen([path, "-v", "0"])
    print(f"已启动：{path}")


# 【核心】把原有执行逻辑抽成独立函数，只写一次
def ark():

    launch_game("zhongmodi", "终末地")

    hwnd = function.get_target_window_hwnd("Endfield")


    function.force_foreground_window(hwnd)

    sleep(50)


    # 点击1并验证2，过5秒
    function.pic_operate_with_check(r"ark_img\1.png", r"ark_img\2.png")
    sleep(5)

    # 点击3
    function.click_pic(r"ark_img\3.png")

    # 然后为了确保在主页面，一直点击esc，直到验证5，过1秒
    while True:
        pydirectinput.press("esc")
        sleep(1)
        if function.check_pic_exist(r"ark_img\5.png"):
            break

    # 这里再按一下esc，等一秒
    pydirectinput.press("esc")
    sleep(1)

    # 按下m，等2秒
    pydirectinput.press("m")
    sleep(2)

    # 如果 34存在，则继续，如果不存在就绝对点击2300，167并验证36，点击36并验证37，点击37并验证2
    if function.check_pic_exist(r"ark_img\34.png"):
        print("存在34")
    else:
        function.click_abs_with_check(2300, 167, r"ark_img\36.png")
        function.pic_operate_with_check(r"ark_img\36.png", r"ark_img\37.png")
        function.pic_operate_with_check(r"ark_img\37.png", r"ark_img\2.png")


    # 按下esc直到验证5
    while True:
        pydirectinput.press("esc")
        sleep(1)
        if function.check_pic_exist(r"ark_img\5.png"):
            break

    # 点击5并验证6，过1秒
    function.pic_operate_with_check(r"ark_img\5.png", r"ark_img\6.png")
    sleep(1)

    # 点击6并验证7，过1秒
    function.pic_operate_with_check(r"ark_img\6.png", r"ark_img\7.png")
    sleep(1)

    # 点击7
    function.click_pic(r"ark_img\7.png")
    sleep(0.5)
    # 点击8并验证9，过1秒
    function.pic_operate_with_check(r"ark_img\8.png", r"ark_img\9.png")
    sleep(1)

    # 击9并验证10，过1秒
    function.pic_operate_with_check(r"ark_img\9.png", r"ark_img\10.png")
    sleep(1)

    # 点击绝对坐标2290，1150，过一秒
    pydirectinput.click(2290, 1150)
    sleep(1)

    # 点击10并验证11，过1秒
    function.pic_operate_with_check(r"ark_img\10.png", r"ark_img\11.png")
    sleep(1)

    # 点击11并验证12，过1秒
    function.pic_operate_with_check(r"ark_img\11.png", r"ark_img\12.png")
    sleep(1)

    # 点击12
    function.click_pic(r"ark_img\12.png")
    sleep(0.5)

    # 点击绝对坐标2290，1150，过一秒
    pydirectinput.click(2290, 1150)
    sleep(1)

    # 点击10并验证11，过1秒
    function.pic_operate_with_check(r"ark_img\10.png", r"ark_img\11.png")
    sleep(1)

    # 点击11，过一秒
    function.click_pic(r"ark_img\11.png")
    sleep(1)

    # 点击esc并验证13，过1秒
    function.press_key_with_check("esc", r"ark_img\13.png")
    sleep(1)

    # 点击13并验证14，过1秒
    function.pic_operate_with_check(r"ark_img\13.png", r"ark_img\14.png")
    sleep(1)

    # 点击14并验证15，过1秒
    function.pic_operate_with_check(r"ark_img\14.png", r"ark_img\15.png")
    sleep(1)

    # 点击15
    function.click_pic(r"ark_img\15.png")
    sleep(0.5)

    # 点击绝对坐标250，1050并验证16，过1秒
    function.click_abs_with_check(250, 1050, r"ark_img\16.png")
    sleep(1)


    # 点击绝对坐标1330，1000
    pydirectinput.click(1330, 1000)
    sleep(0.5)

    # 点击16并验证11，过1秒，这里的十六需要更换一个更好的图，不然识别到其他地方
    function.pic_operate_with_check(r"ark_img\a1.png", r"ark_img\11.png")
    sleep(1)

    #点击11，过1s
    function.click_pic(r"ark_img\11.png")
    sleep(1)

    # 按esc并验证9，过1s
    function.press_key_with_check("esc", r"ark_img\9.png")
    sleep(1)

    # 按下esc并验证5，过1s
    function.press_key_with_check("esc", r"ark_img\5.png")
    sleep(1)

    # 按下esc,等待2s
    pydirectinput.press("esc")
    sleep(2)

    # 按下b并验证17，过1s
    function.press_key_with_check("b", r"ark_img\17.png")
    sleep(1)

    # 点击17并验证18，过1s
    function.pic_operate_with_check(r"ark_img\17.png", r"ark_img\18.png")
    sleep(1)

    # 点击18并验证11，过1s
    function.pic_operate_with_check(r"ark_img\18.png", r"ark_img\11.png")
    sleep(1)

    # 点击11并验证18，过1s
    function.pic_operate_with_check(r"ark_img\11.png", r"ark_img\18.png")
    sleep(1)

    # 按下esc并验证17，过1s
    function.press_key_with_check("esc", r"ark_img\17.png")
    sleep(1)

    # 按下esc,过1s
    pydirectinput.press("esc")
    sleep(1)

    # 按下n并验证19，过1s
    function.press_key_with_check("n", r"ark_img\19.png")
    sleep(1)

    # 点击19并验证20，过1s
    function.pic_operate_with_check(r"ark_img\19.png", r"ark_img\20.png")
    sleep(1)


    # 点击20过一秒
    function.click_pic(r"ark_img\20.png")
    sleep(1)

    # 点击21过一秒
    function.click_pic(r"ark_img\21.png")
    sleep(1)

    # 点击22并验证23，过2秒
    function.pic_operate_with_check(r"ark_img\22.png", r"ark_img\23.png")
    sleep(2)

    # 单纯点击一下然后验证24
    pydirectinput.click()
    sleep(1.5)
    while True:
        if function.check_pic_exist(r"ark_img\24.png"):
            break
        else:
            pydirectinput.click()
            sleep(1)
    # 点击绝对坐标140，1200并验证25，过1秒
    function.click_abs_with_check(140, 1200, r"ark_img\25.png")
    sleep(1)

    # 点击25并验证26，过1秒
    function.pic_operate_with_check(r"ark_img\25.png", r"ark_img\26.png")
    sleep(1)

    #点击27并验证23，过1秒
    function.pic_operate_with_check(r"ark_img\27.png", r"ark_img\23.png")
    sleep(1)

    # 按下esc过1秒
    pydirectinput.press("esc")
    sleep(1)

    # 按下esc并验证28，过1秒
    function.press_key_with_check("esc", r"ark_img\28.png")
    sleep(1)

    # 按下esc过1秒
    pydirectinput.press("esc")
    sleep(1)

    # 按下i并验证29，过1秒
    function.press_key_with_check("i", r"ark_img\29.png")
    sleep(1)

    # 按下29并验证11，过1秒
    function.pic_operate_with_check(r"ark_img\29.png", r"ark_img\11.png")
    sleep(1)

    # 按下11
    function.click_pic(r"ark_img\11.png")
    sleep(1)
    # 按下30并验证31，过1秒
    # 按下esc，等待1s
    pydirectinput.press("esc")
    sleep(1)

    # 按下f8并验证32，过1秒
    function.press_key_with_check("f8", r"ark_img\32.png")
    sleep(1)

    #按下32并验证33，过1秒
    function.pic_operate_with_check(r"ark_img\32.png", r"ark_img\33.png")
    sleep(1)

    # 按下33并验证11，过1秒
    function.pic_operate_with_check(r"ark_img\33.png", r"ark_img\11.png")
    sleep(1)

    # 点击11
    function.click_pic(r"ark_img\11.png")



# 给 main.py 调用的入口


def main(game_path=None, config_key=None):
    ark()  # 直接调用复用


# 本地单独运行脚本时执行
if __name__ == "__main__":
    ark()  # 同样调用复用
