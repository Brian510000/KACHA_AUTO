import tkinter as tk
from tkinter import simpledialog, messagebox
import share
import subprocess
import os
import sys
import json
# ========== 配色 ==========
COLORS = {
    "bg": "#F7F6F3",
    "card": "#FFFFFF",
    "card_hover": "#F0F4F8",
    "card_press": "#E4EBF2",
    "text_primary": "#2C313A",
    "text_secondary": "#8A9099",
}

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
        

def _run_generic(config_key: str, game_name: str, script_name: str):
    """通用运行函数：加载/设置路径，并启动指定的脚本"""
    # 1. 加载已有配置
    saved_path = load_path(config_key)

    if saved_path:
        path = saved_path.strip()
        print(f"使用已保存的 {game_name} 路径：{path}")
    else:
        # 首次使用，弹出输入框
        path = simpledialog.askstring(
            title=f"设置{game_name}路径",
            prompt=f"请输入{game_name}游戏的绝对路径（可执行文件或目录）："
        )
        if not path or not path.strip():
            if path is not None:
                messagebox.showwarning("提示", "路径不能为空~")
            return
        path = path.strip()

        if save_path(config_key, path):
            messagebox.showinfo("保存成功", f"{game_name}路径已永久保存：\n{path}")
        else:
            messagebox.showerror("保存失败", "无法写入配置文件，请检查权限")
            return



    # 3. 运行指定脚本
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        target_script = os.path.join(script_dir, script_name)
        if not os.path.exists(target_script):
            messagebox.showerror("错误", f"未找到脚本：{target_script}")
            return

        # 使用 subprocess.run 捕获错误（调试用）
        proc = subprocess.Popen(
            [sys.executable, target_script, path, config_key],
            cwd=script_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"已启动 {game_name} 脚本 (PID: {proc.pid})")

    except Exception as e:
        messagebox.showerror("启动失败", str(e))



class MinimalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KACHA AUTO")
        self.root.geometry("720x500")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)
        self.center_window()

        # 标题
        header = tk.Frame(root, bg=COLORS["bg"])
        header.pack(pady=(45, 35))
        tk.Label(header, text="KACHA", font=("Georgia", 30, "bold"),
                 fg=COLORS["text_primary"], bg=COLORS["bg"]).pack()
        tk.Label(header, text="Automation Toolkit", font=("Georgia", 10),
                 fg=COLORS["text_secondary"], bg=COLORS["bg"]).pack(pady=(4, 0))

        # 按钮网格
        grid = tk.Frame(root, bg=COLORS["bg"])
        grid.pack(padx=60, fill="both", expand=True)

        features = ["终末地", "异环", "鸣潮",
                    "FGO", "农世界", "NIKKE"]

        for i, name in enumerate(features):
            row, col = divmod(i, 3)
            btn = self.create_card(grid, name)
            btn.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        for r in range(2):
            grid.grid_rowconfigure(r, weight=1)

        # 底部
        tk.Label(root, text="Version 1.0.0", font=("Georgia", 9),
                 fg=COLORS["text_secondary"], bg=COLORS["bg"]).pack(pady=(20, 30))

    # ========== ↓↓↓ 在这里写你的功能函数 ↓↓↓ ==========

    def run_zhongmodi(self):
        _run_generic("zhongmodi", "终末地", "ArkAuto.py")


    def run_yihuan(self):
        """异环脚本：加载或设置路径，并运行 test.py"""
        _run_generic("yihuan", "异环", "NteAuto.py")   # 指定脚本

    def run_mingchao(self):
        """鸣潮脚本"""
        print("运行：鸣潮 脚本")

    def run_fgo(self):
        """FGO脚本"""
        _run_generic("fgo", "FGO", "FgoAuto.py")   # 指定脚本

    def run_nongshijie(self):
        """农世界脚本"""
        print("运行：农世界 脚本")

    def run_nikke(self):
        """NIKKE脚本"""
        _run_generic("nikke", "NIKKE", "NikkeAuto.py")

    # ========== ↑↑↑ 功能函数写这里 ↑↑↑ ==========

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def create_card(self, parent, name):
        """纯文字直角卡片按钮"""
        w, h = 180, 120
        canvas = tk.Canvas(parent, width=w, height=h + 4,
                           bg=COLORS["bg"], highlightthickness=0, cursor="hand2")

        # 卡片背景
        card = canvas.create_rectangle(
            0, 0, w, h, fill=COLORS["card"], outline="")

        # 主标题
        title = canvas.create_text(w // 2, h // 2 - 8, text=name,
                                   font=("微软雅黑", 15, "bold"),
                                   fill=COLORS["text_primary"])

        # 英文小字
        sub = canvas.create_text(w // 2, h // 2 + 16, text=name.upper(),
                                 font=("Georgia", 8),
                                 fill=COLORS["text_secondary"])

        items = [card, title, sub]
        offset = 0

        # 按钮名 → 函数的映射表
        func_map = {
            "终末地": self.run_zhongmodi,
            "异环": self.run_yihuan,
            "鸣潮": self.run_mingchao,
            "FGO": self.run_fgo,
            "农世界": self.run_nongshijie,
            "NIKKE": self.run_nikke,
        }

        def on_enter(_):
            canvas.itemconfig(card, fill=COLORS["card_hover"])

        def on_leave(_):
            nonlocal offset
            if offset:
                for item in items:
                    canvas.move(item, 0, -offset)
                offset = 0
            canvas.itemconfig(card, fill=COLORS["card"])

        def on_press(_):
            nonlocal offset
            if not offset:
                canvas.itemconfig(card, fill=COLORS["card_press"])
                for item in items:
                    canvas.move(item, 0, 2)
                offset = 2

        def on_release(_):
            nonlocal offset
            if offset:
                for item in items:
                    canvas.move(item, 0, -offset)
                offset = 0
                canvas.itemconfig(card, fill=COLORS["card_hover"])
                # ========== 点击后运行对应的函数 ==========
                if name in func_map:
                    func_map[name]()  # 调用对应函数

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease-1>", on_release)

        return canvas


if __name__ == "__main__":
    root = tk.Tk()
    MinimalApp(root)
    root.mainloop()
