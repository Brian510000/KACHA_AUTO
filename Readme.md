![1784135621924](image/Readme/1784135621924.png)

![1784135679159](image/Readme/1784135679159.png)

![1784135692918](image/Readme/1784135692918.png)

![1784135715688](image/Readme/1784135715688.png)



每一份py文件的开头都要记得


```python
# ========== 全局初始化（解决Windows缩放偏移） ==========
ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
pyautogui.PAUSE = 0.2  # 操作间隔，防操作过快

# ========== 配置项 ==========
IMG_CONFIDENCE = 0.8
RETRY_DELAY = 1
MAX_RETRY = 30  # 不建议无限重试
```


记得把句柄的获取放在外面保存

`hwnd = function.get_target_window_hwnd(window_keyword)`

目前写的都是针对于全屏，小窗的话应对方案的焦点加移动窗口到左上角
