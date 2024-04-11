# mamba create -n LunaHook_log python=3.10 pillow -c conda-forge
import os
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkf
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
        "codepage_real": [932, 936, 65001, 1200, 12000, 950],
    }
    encoding_list = [
        'shift_jis',
        'gbk',
        'utf-8',
        'utf-16-le',
        'utf-32-le',
        'big5',
    ]
    encoding_list2static_data = {

    }
    selectedp: tuple
    savehook_new_data: dict

    hook: texthook = None
    allHooks: dict

    callback_list = []

    def callback(*args):
        print('Cfg.callback', *args)
        for cb in Cfg.callback_list:
            cb(*args)


def _updateDdbHooks(_ddb, _hooks):
    _ddb['value'] = _hooks
    if not 0 <= _ddb.current() < len(_hooks):
        _ddb.current(0)


def updateAllHooks():
    _tmp = Cfg.hook.hookdatacollecter
    _hooks = {}
    for key in _tmp.keys():
        if key[4] not in _hooks:
            _hooks[key[4]] = {key[5]}
        else:
            _hooks[key[4]].add(key[5])
    print(_hooks)
    Cfg.allHooks = _hooks
    if _hooks:
        _hooks = list(_hooks.keys())
        _updateDdbHooks(Windows.ddb_char_k, _hooks)
        _updateDdbHooks(Windows.ddb_content_k, _hooks)

        _hooks = list(Cfg.allHooks[Windows.ddb_char_k.get()])
        _updateDdbHooks(Windows.ddb_char_v, _hooks)
        _hooks = list(Cfg.allHooks[Windows.ddb_content_k.get()])
        _updateDdbHooks(Windows.ddb_content_v, _hooks)


class Windows:
    # ===== dll目录 =====
    label_hook_dll_path: tk.Label
    button_hook_dll_root: tk
    # ===== 选择进程 =====
    ddb_AttachProcess_codepage: ttk.Combobox
    button_AttachProcess: tk.Button
    label_AttachProcessPID: tk.Label
    # ===== 搜索钩子 =====
    button_findhook: tk.Button
    ddb_findhook_codepage: ttk.Combobox
    entry_findhook: tk.Entry
    # ===== 注入钩子 =====
    button_inserthook: tk.Button
    entry_inserthook: tk.Entry
    # ===== 人物 =====
    ddb_char: ttk.Combobox
    ddb_char_k: ttk.Combobox
    ddb_char_v: ttk.Combobox
    # ===== 内容 =====
    ddb_content: ttk.Combobox
    ddb_content_k: ttk.Combobox
    ddb_content_v: ttk.Combobox
    button_content: tk.Button
    # ===== 捕获输出 =====
    label_cb_n: tk.Label
    label_cb_d: tk.Label

    root = tk.Tk()


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.1 " + "管理员" if windows.IsUserAnAdmin() else "非管理员")  # 窗口名
Windows.root.geometry('640x320+10+10')  # axb为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
# Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

# ===== dll目录 =====
Windows.label_hook_dll_root = tk.Label(Windows.root, text=Cfg.hook_dll_path)
Windows.label_hook_dll_root.grid(row=99, column=1, columnspan=4)


def button_hook_dll_root():
    _askd_hook_dll_root = tkf.askdirectory(
        title='LunaHost.dll的目录',
        initialdir=Cfg.hook_dll_root
    )
    if not _askd_hook_dll_root:
        return
    _askd_hook_dll_root = os.path.abspath(_askd_hook_dll_root)
    Cfg.hook_dll_root = _askd_hook_dll_root
    Cfg.hook_dll_path = os.path.join(_askd_hook_dll_root,
                                     ("LunaHost32.dll", "LunaHost64.dll")[Cfg.isbit64])
    Windows.label_hook_dll_root.config(text=Cfg.hook_dll_path)


Windows.button_hook_dll_root = tk.Button(
    Windows.root,
    text='选择 LunaHook 目录',
    command=button_hook_dll_root
)
Windows.button_hook_dll_root.grid(row=99, column=0)
# ===== 选择进程 =====
Windows.label_AttachProcessPID = tk.Label(Windows.root, text=f'等待注入进程')
Windows.label_AttachProcessPID.grid(row=0, column=1)


def ddb_encoding_list(_current=0):
    _ddb = ttk.Combobox(Windows.root)
    _ddb['value'] = Cfg.encoding_list
    _ddb.current(_current)
    return _ddb


Windows.ddb_AttachProcess_codepage = ddb_encoding_list(1)
Windows.ddb_AttachProcess_codepage.grid(row=0, column=0)


# ===== 注入进程 =====
def button_AttachProcess():
    Cfg.selectedp = getAttachProcess(Windows.root)
    Cfg.savehook_new_data = {Cfg.selectedp[1]: getdefaultsavehook(Cfg.selectedp[1])}
    _idx = Windows.ddb_AttachProcess_codepage.current()
    print(Cfg.static_data['codepage_real'][_idx], Windows.ddb_AttachProcess_codepage.get())
    Cfg.savehook_new_data[Cfg.selectedp[1]]['codepage'] = Cfg.static_data['codepage_real'][_idx]
    Windows.label_AttachProcessPID.config(text=f'进程号:  {Cfg.selectedp[0]}')
    Cfg.hook = texthook(Cfg.selectedp[0], Cfg.selectedp[2], Cfg.selectedp[1], Cfg=Cfg)
    print(Cfg.hook)


Windows.button_AttachProcess = tk.Button(Windows.root, text='注入进程', command=button_AttachProcess)
Windows.button_AttachProcess.grid(row=0, column=2)


# ===== 搜索钩子 =====
def button_findhook():
    _usestruct = Cfg.hook.defaultsp()
    _usestruct.codepage = int(Windows.ddb_findhook_codepage.get())
    _usestruct.text = Windows.entry_findhook.get()
    print('搜索钩子', _usestruct.codepage, _usestruct.text)
    Cfg.hook.findhook(_usestruct)


Windows.ddb_findhook_codepage = ttk.Combobox(Windows.root)
Windows.ddb_findhook_codepage['value'] = Cfg.static_data['codepage_real']
Windows.ddb_findhook_codepage.current(0)
Windows.ddb_findhook_codepage.grid(row=1, column=0)
Windows.entry_findhook = tk.Entry(Windows.root)
Windows.entry_findhook.grid(row=1, column=1)
Windows.button_findhook = tk.Button(Windows.root, text='搜索钩子', command=button_findhook)
Windows.button_findhook.grid(row=1, column=2)


# ===== 注入钩子 =====
def button_inserthook():
    print('注入钩子', Windows.entry_inserthook.get())
    Cfg.hook.inserthook(Windows.entry_inserthook.get())


Windows.entry_inserthook = tk.Entry(Windows.root)
Windows.entry_inserthook.grid(row=2, column=1)
Windows.button_inserthook = tk.Button(Windows.root, text='注入钩子', command=button_inserthook)
Windows.button_inserthook.grid(row=2, column=2)

# ===== 人物 =====
Windows.ddb_char = ddb_encoding_list(0)
Windows.ddb_char.grid(row=3, column=0)

Windows.ddb_char_k = ttk.Combobox()
Windows.ddb_char_k.grid(row=3, column=1)

Windows.ddb_char_v = ttk.Combobox()
Windows.ddb_char_v.grid(row=3, column=2)


@Windows.root.register
def ddb_char_v_update():
    _hooks = list(Cfg.allHooks[Windows.ddb_char_k.get()])
    _updateDdbHooks(Windows.ddb_char_v, _hooks)


Windows.ddb_char_k.bind('<<ComboboxSelected>>', ddb_char_v_update)


@Windows.root.register
def check_digit(content):
    if content.isdigit() or content == "":
        return True
    else:
        return False


# ===== 内容 =====
Windows.ddb_content = ddb_encoding_list(1)
Windows.ddb_content.grid(row=4, column=0)

Windows.ddb_content_k = ttk.Combobox()
Windows.ddb_content_k.grid(row=4, column=1)

Windows.ddb_content_v = ttk.Combobox()
Windows.ddb_content_v.grid(row=4, column=2)


@Windows.root.register
def ddb_content_v_update():
    _hooks = list(Cfg.allHooks[Windows.ddb_content_k.get()])
    _updateDdbHooks(Windows.ddb_content_v, _hooks)


Windows.ddb_content_k.bind('<<ComboboxSelected>>', ddb_content_v_update)


def button_content():
    updateAllHooks()


Windows.button_content = tk.Button(
    Windows.root,
    text='更新钩子列表',
    command=button_content
)
Windows.button_content.grid(row=4, column=3)

# ===== 捕获输出 =====
Windows.label_cb_n = tk.Label(Windows.root, text=f'旁白')
Windows.label_cb_n.grid(row=97, columnspan=4, sticky=tk.W)


def cb_n(key, output: str):
    if key[4] == Windows.ddb_char_k.get() and key[5] == Windows.ddb_char_v.get():
        if Windows.ddb_AttachProcess_codepage.get() != Windows.ddb_char.get():
            tmp = output.encode(
                Windows.ddb_AttachProcess_codepage.get(), errors='ignore'
            ).decode(Windows.ddb_char.get(), errors='ignore')
        else:
            tmp = output
        Windows.label_cb_n.config(text=tmp)


Cfg.callback_list.append(cb_n)

Windows.label_cb_d = tk.Label(Windows.root, text=f'内容')
Windows.label_cb_d.grid(row=98, columnspan=4, sticky=tk.W)


def cb_d(key, output):
    if key[4] == Windows.ddb_content_k.get() and key[5] == Windows.ddb_content_v.get():
        if Windows.ddb_AttachProcess_codepage.get() != Windows.ddb_content.get():
            tmp = output.encode(
                Windows.ddb_AttachProcess_codepage.get(), errors='ignore'
            ).decode(Windows.ddb_content.get(), errors='ignore')
        else:
            tmp = output
        Windows.label_cb_d.config(text=tmp)


Cfg.callback_list.append(cb_d)


# ===== 时钟循环 =====
def clock_loop():
    if Cfg.hook is not None:
        _tmp = Cfg.hook.hookdatacollecter
        if _tmp:
            button_content()
            return
    Windows.root.after(500, clock_loop)


Windows.root.after(500, clock_loop)
# ===== 进入消息循环 =====
Windows.root.mainloop()
