import win32gui
import share
import subprocess
import os
import function
import pyautogui
import ctypes
import pydirectinput
from time import sleep
from main import load_path
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


# 首先是启动猫猫云的脚本,然后才轮到启动游戏

# 想要稳定启动猫猫云，就必须先结束掉所有猫猫云进程
def kill_maomaoyun():
    # Windows 调用 taskkill 强杀
    cmd = r'taskkill /F /IM "猫猫云.exe" /T'
    subprocess.run(cmd, shell=True, check=False)
    print("猫猫云进程已全部结束")


# 使用
kill_maomaoyun()

# 路径建议用原始字符串 / 双反斜杠
exe_path = r"C:\Users\Brian\AppData\Local\Programs\MAOMAOYUNAPP\猫猫云.exe"

# 方式1：基础调用（推荐）
subprocess.Popen(
    exe_path,
    cwd=os.path.dirname(exe_path),  # 指定工作目录为程序所在文件夹
    encoding="utf-8",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
sleep(5)
print("启动猫猫云成功")
hwnd = function.get_target_window_hwnd("已就绪")
print(f"猫猫云窗口句柄：{hwnd}")
function.force_foreground_window(hwnd)
sleep(1)
function.window_pic_operate_with_check(r"img\0.png", r"img\1.png", hwnd)
print("接下来启动nikke启动器")


launch_game("nikke", "NIKKE")
hwnd = function.get_target_window_hwnd("NIKKE")
function.force_foreground_window(hwnd)

# 移动窗口到 坐标(0, 0)，宽高保持原有大小
# 语法：SetWindowPos(句柄, 置顶层级, x, y, 宽度, 高度, 标志位)
# SWP_NOSIZE = 0x0001 保持原有宽高，不修改尺寸
win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001)
# 这里等待登录，正式进入启动器
sleep(10)
hwnd = function.get_target_window_hwnd("NIKKE")
function.force_foreground_window(hwnd)
win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001)

# 先点击绝对坐标292，1202，等10秒，然后循环找句柄来置顶nikke
pydirectinput.click(292,1202)
sleep(15)

hwnd = function.get_target_window_hwnd("NIKKE")
function.force_foreground_window(hwnd)
win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
# 然后一直点绝对坐标292,1201，直到验证图片2
while True:
    pydirectinput.click(292,1201)
    sleep(1)
    if function.check_pic_exist(r"Nikke_img/2.png"):
        pydirectinput.click(292,1201)
        break
# 等待1秒
sleep(1)
# 点击2并验证3，等待一秒
function.pic_operate_with_check(r"Nikke_img/2.png", r"Nikke_img/3.png")
sleep(1)
# 点击3并验证4，
function.pic_operate_with_check(r"Nikke_img/3.png", r"Nikke_img/4.png")
sleep(1)

# 点击4
function.click_pic(r"Nikke_img/4.png")
sleep(0.5)
# 一直按esc直到验证1
while True:
    pydirectinput.press('esc')
    sleep(0.5)
    if function.check_pic_exist(r"Nikke_img/1.png"):
        # 按下esc，等待0.5s
        pydirectinput.press('esc')
        sleep(1)
        break

# 点击绝对坐标764，985，然后验证5，等待1s
function.click_abs_with_check(764, 985, r"Nikke_img/5.png")
sleep(1)
#点击绝对坐标270，988，然后验证6，等待1s
function.click_abs_with_check(270, 988, r"Nikke_img/6.png")
sleep(1)



#点击6并验证7，等待1s
function.pic_operate_with_check(r"Nikke_img/6.png", r"Nikke_img/7.png")
sleep(1)

# 点击7并验证5，等待1s
function.pic_operate_with_check(r"Nikke_img/7.png", r"Nikke_img/5.png")
sleep(1)

# 点击5并验证8，等待1s
function.pic_operate_with_check(r"Nikke_img/5.png", r"Nikke_img/8.png")
sleep(1)

# 点击8并验证6，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/8.png", r"Nikke_img/6.png", 1.0)


# 点击6并验证9，等待1s（这里感觉7和9并不太一样）
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/6.png", r"Nikke_img/9.png", 1.0)


# 点击9并验证10，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/9.png", r"Nikke_img/10.png", 1.0)


# 一直按esc直到验证1
# 按下esc，等待0.5s
while True:
    pydirectinput.press('esc')
    sleep(0.5)
    if function.check_pic_exist(r"Nikke_img/1.png"):
        # 按下esc，等待0.5s
        pydirectinput.press('esc')
        sleep(1)
        break
# 点击绝对坐标（前哨基地）789，1118并验证11，等待1s
function.click_abs_with_check(789, 1118, r"Nikke_img/11.png")
sleep(1)
# 点击11并验证12，等待1s(这里点击11并不能进入，感觉还是点绝对坐标吧)1335，1355
function.click_abs_with_check(1335, 1355, r"Nikke_img/12.png")
sleep(1)
# 点击12并验证13，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/12.png", r"Nikke_img/13.png", 1.0)
# 点击13并验证14，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/13.png", r"Nikke_img/14.png", 1.0)
# 点击14并验证15，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/14.png", r"Nikke_img/15.png", 1.0)
# 点击15并验证16，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/15.png", r"Nikke_img/16.png", 1.0)
# 按下esc并验证11，等待0.5s
function.press_key_with_check('esc', r"Nikke_img/11.png")
sleep(0.5)


# 点击绝对坐标2385，1350并验证17，等待1s
function.click_abs_with_check(2385, 1350, r"Nikke_img/17.png")
sleep(1)
# 点击17并验证18，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/17.png", r"Nikke_img/18.png", 1.0)

# 点击18并验证19，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/18.png", r"Nikke_img/19.png", 1.0)
# 点击19并验证20，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/19.png", r"Nikke_img/20.png", 1.0)
# 点击20并验证21，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/20.png", r"Nikke_img/21.png", 1.0)
# 点击21并验证23，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/21.png", r"Nikke_img/23.png", 1.0)
# 点击23并验证11，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/23.png", r"Nikke_img/11.png", 1.0)
# 点击24并验证25，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/24.png", r"Nikke_img/25.png", 1.0)
# 点击25并验证26，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/25.png", r"Nikke_img/26.png", 1.0)


# 点击26并验证27，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/26.png", r"Nikke_img/27.png", 1.0)




# 点击绝对坐标1278，850并验证28，等1s
function.click_abs_with_check(1278, 850, r"Nikke_img/28.png")
sleep(1)
# 点击28并验证29，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/28.png", r"Nikke_img/29.png", 1.0)
# 点击29并验证27，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/29.png", r"Nikke_img/27.png", 1.0)
# 按下esc并验证30，等待0.5s
function.press_key_with_check('esc', r"Nikke_img/30.png")
sleep(0.5)
# 点击30并验证31，等待1s
function.pic_operate_with_check_with_success_sleep(r"Nikke_img/30.png", r"Nikke_img/31.png", 1.0)
# 点击绝对坐标1280，1170并验证32，等待1s
function.click_abs_with_check(1280, 1170, r"Nikke_img/32.png")
sleep(1)


# 点击32的绝对坐标1492，1214，一直点击直到验证33

# 一直按esc直到验证34

# 点击绝对坐标1540，657并验证35，等待1s

# 点击35并验证36，等待1s

# 点击36并验证34，等待1s

# 一直按esc直到验证1
# 按下esc，等待0.5s

# 点击绝对坐标1570，1318并验证37，等待1s

# 点击37并验证38，等待1s

# 点击38，这里需要等久一点，然后验证39

# 点击39并验证40，等待1s

# 点击40，等待1s

# 按下esc并验证24，等待0.5s

# 点击24并验证25，等待1s

# 点击25并验证41，等待1s

# 点击绝对坐标1280，927，并验证25，等待1s

# 点击25



