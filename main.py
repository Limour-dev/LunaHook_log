# mamba create -n LunaHook_log python=3.10 pillow -c conda-forge
import os
import platform
import tkinter
from mods.m02_lunahook import texthook


class Cfg:
    isbit64 = (platform.architecture()[0] == "64bit")
    hook_dll_root: str = r'D:\scn\LunaTranslator\Release_Chinese'
    hook_dll_root = os.path.abspath(hook_dll_root)
    hook_dll_path = os.path.join(hook_dll_root,
                                 ("LunaHost32.dll", "LunaHost64.dll")[isbit64])
    globalconfig = {
        "allow_set_text_name": False,
        "use_yapi": True,
        "embedded": {
            "safecheck_use": True,
            "safecheckregexs": [
                "(.*?)\\{(.*?)\\}(.*?)",
                "(.*?)\\[(.*?)\\](.*?)"
            ],
            "timeout_translate": 2,
            "changefont": False,
            "changefont_font": "",
            "insertspace_policy": 0,
            "keeprawtext": False,
        },
        "autorun": True,
        "textthreaddelay": 500,
        "direct_filterrepeat": False,
        "flushbuffersize": 3000,
        "filter_chaos_code": False,
    }
    static_data = {
        "codepage_real": [932, 65001, 936, 950, 949, 1258, 874, 1256, 1255, 1254, 1253, 1257, 1250, 1251, 1252, 437],
    }


class Windows:
    label_hook_dll_path: tkinter.Label
    root = tkinter.Tk()


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.1")  # 窗口名
Windows.root.geometry('480x160+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
# Windows.root.attributes("-alpha", 0.5)  # 设置窗口半透明

# ===== 绘制窗口控件 =====
Windows.label_hook_dll_path = tkinter.Label(Windows.root, text=f'Cfg.hook_dll_path: {Cfg.hook_dll_path}')
Windows.label_hook_dll_path.grid(row=0, column=0)

# ===== 进入消息循环 =====
Windows.root.mainloop()
