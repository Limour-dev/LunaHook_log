# mamba create -n LunaHook_log python=3.10 pillow -c conda-forge
import os
import platform
import tkinter
from tkinter import ttk
from mods.m02_lunahook import texthook
from mods.m05_attachprocess import getAttachProcess
import mods.m03_windows as windows


def getdefaultsavehook(gamepath, title=None):
    default = {
        "localeswitcher": 0,
        "onloadautochangemode2": 0,
        "onloadautoswitchsrclang": 0,
        "needinserthookcode": [],
        "embedablehook": [],
        "imagepath": None,
        "infopath": None,
        "vid": 0,
        "statistic_playtime": 0,
        "statistic_wordcount": 0,
        "statistic_wordcount_nodump": 0,
        "leuse": True,
        "startcmd": '"{exepath}"',
        "startcmduse": False,
        "hook": [],
        "inserthooktimeout": 0,
        "needinserthookcode": [],
        "removeuseless": False,
        "codepage_index": 0,
        "allow_tts_auto_names": "",
        "tts_repair": False,
        "tts_repair_regex": [],
        "hooktypeasname": {},
        "use_saved_text_process": False,
        "searchnoresulttime": 0,
        "relationlinks": [],
        "gamejsonfile": "",
        "gamesqlitefile": "",
        "gamexmlfile": "",
    }
    if gamepath == "0":
        default["title"] = "No Game"
    elif title and len(title):
        default["title"] = title
    else:
        default["title"] = (
                os.path.basename(os.path.dirname(gamepath))
                + "/"
                + os.path.basename(gamepath)
        )
    return default


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
    selectedp = getAttachProcess()
    savehook_new_data = {selectedp[1]: getdefaultsavehook(selectedp[1])}
    hook: texthook


class Windows:
    label_hook_dll_path: tkinter.Label
    button_AttachProcess: tkinter.Button
    label_AttachProcessPID: tkinter.Label
    button_findhook: tkinter.Button
    ddb_findhook_codepage: ttk.Combobox
    entry_findhook: tkinter.Entry
    button_inserthook: tkinter.Button
    entry_inserthook: tkinter.Entry
    root = tkinter.Tk()


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.1 " + "管理员" if windows.IsUserAnAdmin() else "非管理员")  # 窗口名
Windows.root.geometry('480x160+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
# Windows.root.attributes("-alpha", 0.5)  # 设置窗口半透明


# ===== 选择进程 =====
Windows.label_AttachProcessPID = tkinter.Label(Windows.root, text=f'进程号:  {Cfg.selectedp[0]}')
Windows.label_AttachProcessPID.grid(row=0, column=1)


# ===== 注入进程 =====
def button_AttachProcess():
    # Cfg.selectedp = getAttachProcess()
    # Cfg.savehook_new_data = {Cfg.selectedp[1]: getdefaultsavehook(Cfg.selectedp[1])}
    Cfg.hook = texthook(Cfg.selectedp[0], Cfg.selectedp[2], Cfg.selectedp[1], Cfg=Cfg)
    print(Cfg.hook)


Windows.button_AttachProcess = tkinter.Button(Windows.root, text='注入进程', command=button_AttachProcess)
Windows.button_AttachProcess.grid(row=0, column=2)


# ===== 搜索钩子 =====
def button_findhook():
    _usestruct = Cfg.hook.defaultsp()
    _usestruct.codepage = 936
    _usestruct.text = Windows.entry_findhook.get()
    print('搜索钩子', _usestruct.codepage, _usestruct.text)
    Cfg.hook.findhook(_usestruct)


Windows.ddb_findhook_codepage = ttk.Combobox(Windows.root)
Windows.ddb_findhook_codepage['value'] = Cfg.static_data['codepage_real']
Windows.ddb_findhook_codepage.current(0)
Windows.ddb_findhook_codepage.grid(row=1, column=0)
Windows.entry_findhook = tkinter.Entry(Windows.root)
Windows.entry_findhook.grid(row=1, column=1)
Windows.button_findhook = tkinter.Button(Windows.root, text='搜索钩子', command=button_findhook)
Windows.button_findhook.grid(row=1, column=2)


# ===== 注入钩子 =====
def button_inserthook():
    print('注入钩子', Windows.entry_inserthook.get())
    Cfg.hook.inserthook(Windows.entry_inserthook.get())


Windows.entry_inserthook = tkinter.Entry(Windows.root)
Windows.entry_inserthook.grid(row=2, column=1)
Windows.button_inserthook = tkinter.Button(Windows.root, text='注入钩子', command=button_inserthook)
Windows.button_inserthook.grid(row=2, column=2)
# ===== 绘制窗口控件 =====
Windows.label_hook_dll_path = tkinter.Label(Windows.root, text=f'Cfg.hook_dll_path: {Cfg.hook_dll_path}')
Windows.label_hook_dll_path.grid(row=99, columnspan=4, sticky=tkinter.W)
# ===== 进入消息循环 =====
Windows.root.mainloop()
