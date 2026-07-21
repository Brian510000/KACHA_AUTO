import win32con
import win32gui
import pydirectinput
import pyautogui
import ctypes
from pyautogui import locateOnScreen, ImageNotFoundException, moveTo, click, moveRel, press
from time import sleep,time
from retry import retry
import win32process
import os
import sys
import json


# ========== 全局初始化（解决Windows缩放偏移） ==========
ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
pyautogui.PAUSE = 0.2  # 操作间隔，防操作过快

# ========== 配置项 ==========
IMG_CONFIDENCE = 0.8
RETRY_DELAY = 1
MAX_RETRY = 30  # 不建议无限重试
CHECK_MAX_TIMES = 10  # 验证图片最大重试次数
CHECK_INTERVAL = 1    # 验证图片查找间隔(秒)

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".game_paths.json")

def load_path(key: str) -> str:
    if not os.path.exists(CONFIG_FILE):
        return ""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        raw = data.get(key, "")
        # 去除首尾的双引号或单引号
        if raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]
        elif raw.startswith("'") and raw.endswith("'"):
            raw = raw[1:-1]
        return raw
    except:
        return ""


def save_path(key: str, path: str) -> bool:
    """保存指定键的路径到配置文件，返回是否成功"""
    try:
        # 先读取现有数据
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        # 更新键值
        data[key] = path
        # 写回
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False
# ========== 窗口工具 ==========


@retry(exceptions=OSError, delay=1, tries=120)
def get_target_window_hwnd(window_keyword: str):
    """根据窗口关键字获取句柄"""
    hwnd_list = []

    def enum_windows(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if window_keyword in title:
            hwnd_list.append((hwnd, title))
    win32gui.EnumWindows(enum_windows, None)
    if not hwnd_list:
        print(f"未找到包含关键字的窗口")
        raise OSError(f"未找到包含关键字【{window_keyword}】的窗口")
    return hwnd_list[0][0]


def get_window_region(hwnd):
    """获取窗口截图区域 (x, y, width, height)"""
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (left, top, right - left, bottom - top)


def force_foreground_window(hwnd):
    if not win32gui.IsWindow(hwnd):
        return False

    # 1. 如果窗口最小化，先恢复它
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # 2. 获取当前前台窗口的线程 ID
    fore_hwnd = win32gui.GetForegroundWindow()
    fore_tid = win32process.GetWindowThreadProcessId(fore_hwnd)[0]
    target_tid = win32process.GetWindowThreadProcessId(hwnd)[0]

    # 3. 附加线程输入以绕过前台锁定
    if fore_tid != target_tid:
        win32process.AttachThreadInput(target_tid, fore_tid, True)
        win32gui.SetForegroundWindow(hwnd)
        win32process.AttachThreadInput(target_tid, fore_tid, False)
    else:
        win32gui.SetForegroundWindow(hwnd)

    # 4. 强制置顶（关键步骤）
    # 先设为 TOPMOST（置顶），再取消 TOPMOST，这样窗口会“跳到”所有窗口前面
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # 额外保险：再调用一次 BringWindowToTop
    win32gui.BringWindowToTop(hwnd)

    return True

# ========== 主函数 ==========

"""
# (起始X, 起始Y, 区域宽度, 区域高度)
region = SCAN_REGION = (0, 0, 800, 600)
可以用来优化性能,区域找图
"""

#这是窗口的找图,限定了该窗口
@retry(exceptions=pyautogui.ImageNotFoundException, delay=RETRY_DELAY, tries=MAX_RETRY)
def window_click_pic(pic_path: str, hwnd: int):
    region = get_window_region(hwnd)
    locate_pos = pyautogui.locateOnScreen(
        pic_path,
        confidence=IMG_CONFIDENCE,
        region=region
    )
    cx, cy = pyautogui.center(locate_pos)
    pydirectinput.moveTo(cx, cy)
    pydirectinput.click()


#这是全屏找图,可以使用region来优化性能
@retry(exceptions=pyautogui.ImageNotFoundException, delay=RETRY_DELAY, tries=MAX_RETRY)
def click_pic(pic_path: str):
    """找到图片 → 移动到图片中心 → 点击"""
    locate_pos = pyautogui.locateOnScreen(
        pic_path,
        confidence=IMG_CONFIDENCE,
    )
    cx, cy = pyautogui.center(locate_pos)
    pydirectinput.moveTo(cx, cy)
    pydirectinput.click()


@retry(exceptions=pyautogui.ImageNotFoundException, delay=RETRY_DELAY, tries=MAX_RETRY)
def find_pic_and_move(pic_path: str, x_abs: int, y_abs: int):
    """找到图片 → 移动到指定绝对坐标 → 点击"""
    pyautogui.locateOnScreen(
        pic_path,
        confidence=IMG_CONFIDENCE,
    )
    pydirectinput.moveTo(x_abs, y_abs)
    pydirectinput.click()


def pic_operate_with_check(main_pic: str, check_pic: str):
    """
    核心逻辑：
    1. 找到主图片并点击中心
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    """
    while True:
        # 第一步：查找并点击主图片
        click_pic(main_pic)
        # 等待1秒
        sleep(1)

        # 第二步：循环查找验证图片，最多10次
        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        # 验证成功，退出循环；失败则继续外层大循环
        if check_success:
            print(f"验证图片【{check_pic}】找到，操作成功！")
            break


def pic_operate_with_check_with_success_sleep(main_pic: str, check_pic: str, success_sleep: float = 1.0):
    """
    核心逻辑：
    1. 找到主图片并点击中心
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    4. 验证成功后，额外等待指定时长

    :param main_pic: 要点击的主图片路径
    :param check_pic: 用于验证的图片路径
    :param success_sleep: 验证成功后等待的秒数，默认 1.0
    """
    while True:
        # 第一步：查找并点击主图片
        click_pic(main_pic)
        # 等待1秒
        sleep(1)

        # 第二步：循环查找验证图片，最多10次
        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        # 验证成功，退出循环；失败则继续外层大循环
        if check_success:
            print(f"验证图片找到，操作成功！")
            # 新增：验证成功后等待指定时间
            sleep(success_sleep)
            break


def window_pic_operate_with_check(main_pic: str, check_pic: str, hwnd: int = None):
    """
    核心逻辑：
    1. 在指定窗口区域（或全屏）找到主图片并点击中心
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    :param hwnd: 窗口句柄，若为None则全屏查找
    """
    # 根据 hwnd 获取区域
    region = get_window_region(hwnd) if hwnd is not None else None

    while True:
        # 第一步：在区域内查找并点击主图片
        try:
            pos = pyautogui.locateCenterOnScreen(
                main_pic, confidence=IMG_CONFIDENCE, region=region)
            if pos is None:
                # 如果没找到主图片，可能区域不对，重试或报错
                # 这里简单处理，等待后继续外层循环
                print(f"未找到主图片【{main_pic}】，重试...")
                sleep(1)
                continue
            pyautogui.click(pos)
        except pyautogui.ImageNotFoundException:
            print(f"未找到主图片【{main_pic}】，重试...")
            sleep(1)
            continue

        # 等待1秒
        sleep(1)

        # 第二步：循环查找验证图片，最多10次
        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(
                    check_pic, confidence=IMG_CONFIDENCE, region=region)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        if check_success:
            print(f"验证图片【{check_pic}】找到，操作成功！")
            break

# 新增函数：点击图片中心偏移位置 + 校验重试
def pic_click_offset_with_check(main_pic: str, offset_x: int, offset_y: int, check_pic: str):
    """
    核心逻辑：
    1. 找到主图片并点击相对于中心偏移了x,y的位置
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    """
    while True:
        # 1. 查找主图，并点击中心偏移位置
        @retry(exceptions=pyautogui.ImageNotFoundException, delay=RETRY_DELAY, tries=MAX_RETRY)
        def find_and_click_offset():
            pos = pyautogui.locateOnScreen(main_pic, confidence=IMG_CONFIDENCE)
            center_x, center_y = pyautogui.center(pos)
            # 计算偏移后坐标
            target_x = center_x + offset_x
            target_y = center_y + offset_y
            pydirectinput.moveTo(target_x, target_y)
            pydirectinput.click()

        find_and_click_offset()
        sleep(1)

        # 2. 循环查找验证图片，最多10次
        check_ok = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_ok = True
                break
            except pyautogui.ImageNotFoundException:
                time.sleep(CHECK_INTERVAL)

        # 校验通过则退出，不通过则重新走完整流程
        if check_ok:
            print(f"验证图片【{check_pic}】找到，并且点击了偏移位置，操作成功！")
            break


def pic_click_abs_with_check(main_pic: str, x_abs: int, y_abs: int, check_pic: str):
    """
    核心逻辑：
    1. 找到主图片并点击绝对坐标x,y
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    """
    while True:
        # 找到主图，点击指定绝对坐标
        @retry(exceptions=pyautogui.ImageNotFoundException, delay=RETRY_DELAY, tries=MAX_RETRY)
        def find_and_click_abs():
            pyautogui.locateOnScreen(main_pic, confidence=IMG_CONFIDENCE)
            pydirectinput.moveTo(x_abs, y_abs)
            pydirectinput.click()

        find_and_click_abs()
        sleep(1)

        # 循环查找验证图片，最多10次
        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        # 校验通过则退出，失败则重新执行整套流程
        if check_success:
            break


def click_abs_with_check(x_abs: int, y_abs: int, check_pic: str):
    """
    核心逻辑：
    1. 直接点击绝对坐标x,y
    2. 等待1秒，循环10次查找验证图片
    3. 找到验证图片则结束；10次未找到，重新执行整个流程
    """
    while True:
        # 直接移动并点击指定绝对坐标
        pydirectinput.moveTo(x_abs, y_abs)
        pydirectinput.click()
        sleep(1)

        # 循环查找验证图片
        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        if check_success:
            break

def press_key_with_check(key: str, check_pic: str):
    """
    通用按键+验证函数
    :param key: 需要按下的按键，如 "f1"、"enter"、"space"
    :param check_pic: 验证图片路径
    逻辑：按下指定按键 → 等待1秒 → 最多循环10次查找验证图
          找到则结束，未找到则重新执行整套流程
    """
    while True:
        # 按下指定按键
        pydirectinput.press(key)
        sleep(1)

        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(check_pic, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        if check_success:
            break


def window_press_key_with_check(key: str, check_pic: str, hwnd: int = None):
    """
    通用按键+验证函数（支持窗口区域限定）
    :param key: 需要按下的按键，如 "f1"、"enter"、"space"
    :param check_pic: 验证图片路径
    :param hwnd: 窗口句柄，若为None则全屏查找
    逻辑：按下指定按键 → 等待1秒 → 最多循环10次查找验证图
          找到则结束，未找到则重新执行整套流程
    """
    region = get_window_region(hwnd) if hwnd is not None else None

    while True:
        pydirectinput.press(key)
        sleep(1)

        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                pyautogui.locateOnScreen(
                    check_pic, confidence=IMG_CONFIDENCE, region=region)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(CHECK_INTERVAL)

        if check_success:
            break

def press_key_with_two_check(key: str, check_pic1: str, check_pic2: str):
    """
    通用按键+双图验证函数
    :param key: 需要按下的按键，如 "f1"、"enter"、"space"
    :param check_pic1: 验证图片1路径
    :param check_pic2: 验证图片2路径
    逻辑：按下指定按键 → 等待1秒 → 最多循环10次查找验证图
          找到两张图任意一张则结束，都没找到则重新执行整套流程
    """
    while True:
        # 按下指定按键
        pydirectinput.press(key)
        sleep(1)

        check_success = False
        for _ in range(CHECK_MAX_TIMES):
            try:
                # 任意一张存在即验证通过
                pyautogui.locateOnScreen(check_pic1, confidence=IMG_CONFIDENCE)
                check_success = True
                break
            except pyautogui.ImageNotFoundException:
                try:
                    pyautogui.locateOnScreen(
                        check_pic2, confidence=IMG_CONFIDENCE)
                    check_success = True
                    break
                except pyautogui.ImageNotFoundException:
                    sleep(CHECK_INTERVAL)

        if check_success:
            break


def check_pic_exist(pic_path: str) -> int:
    """
    单次检查图片是否存在
    :param pic_path: 图片路径
    :return: 存在返回1，不存在返回0
    """
    try:
        pyautogui.locateOnScreen(pic_path, confidence=IMG_CONFIDENCE)
        return 1
    except pyautogui.ImageNotFoundException:
        return 0


def check_pic_exist_in_times(pic_path: str, timeout: float = 0, hwnd: int = None) -> int:
    """
    在指定时间内持续监测图片是否存在（可限定窗口区域）
    :param pic_path:  图片路径
    :param timeout:   监测时长（秒），若 <=0 则只检测一次
    :param hwnd:      窗口句柄，若为 None 则全屏查找，否则限定在该窗口区域
    :return:          存在返回 1，不存在（超时未出现）返回 0
    """
    # 根据 hwnd 确定查找区域
    region = get_window_region(hwnd) if hwnd is not None else None

    if timeout <= 0:
        # 仅检测一次（兼容原逻辑）
        try:
            pyautogui.locateOnScreen(
                pic_path, confidence=IMG_CONFIDENCE, region=region)
            return 1
        except pyautogui.ImageNotFoundException:
            return 0

    start_time = time()
    while time() - start_time < timeout:
        try:
            pyautogui.locateOnScreen(
                pic_path, confidence=IMG_CONFIDENCE, region=region)
            return 1   # 找到即返回
        except pyautogui.ImageNotFoundException:
            pass       # 未找到，继续循环
        sleep(0.3)  # 检测间隔
    return 0   # 超时仍未找到
