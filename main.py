# mamba create -n LunaHook_log python=3.10 pillow -c conda-forge
# pip install OpenCC -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
import os
import platform
import tkinter as tk
from io import TextIOWrapper
from tkinter import ttk
import tkinter.filedialog as tkf
from tkinter import messagebox
from mods.m02_lunahook import texthook
from mods.m05_attachprocess import getAttachProcess
import mods.m03_windows as windows
from mods.m06_clearT import clearT
import json

_cfg_json = {
    'hook_dll_root': r'D:\scn\LunaTranslator\Release_Chinese',
    'ddb_AttachProcess_codepage': 1,
    'ddb_char': 0,
    'ddb_content': 1,
    'allHooks': {},
    'ddb_char_k': 0,
    'ddb_char_v': 0,
    'ddb_content_k': 0,
    'ddb_content_v': 1,
    'label_log': r'D:\datasets\tmp\1.txt'
}
if os.path.exists('config.json'):
    with open(r'config.json', 'r', encoding='utf-8') as f:
        _cfg_json.update(json.load(f))


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
    hook_dll_root: str
    hook_dll_path: str
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
    allHooks: dict = _cfg_json['allHooks']

    callback_list = []

    def callback(*args):
        print('Cfg.callback', *args)
        for cb in Cfg.callback_list:
            cb(*args)

    log = False
    log_file: TextIOWrapper
    log_add_size: int = 0

    var_n: str = '旁白'
    var_d: str = ''


def _set_hook_dll_root(_askd_hook_dll_root):
    _askd_hook_dll_root = os.path.abspath(_askd_hook_dll_root)
    Cfg.hook_dll_root = _askd_hook_dll_root
    Cfg.hook_dll_path = os.path.join(_askd_hook_dll_root,
                                     ("LunaHost32.dll", "LunaHost64.dll")[Cfg.isbit64])
    Windows.label_hook_dll_root.config(text=Cfg.hook_dll_path)


def _updateDdbHooks(_ddb, _hooks, _current=0):
    _ddb['value'] = _hooks
    if not 0 <= _ddb.current() < len(_hooks):
        _ddb.current(min(_current, len(_hooks) - 1))


def updateAllHooks():
    if Cfg.allHooks:
        _hooks = list(Cfg.allHooks.keys())
        _updateDdbHooks(Windows.ddb_char_k, _hooks, _cfg_json['ddb_char_k'])
        _updateDdbHooks(Windows.ddb_content_k, _hooks, _cfg_json['ddb_content_k'])

        _hooks = list(Cfg.allHooks[Windows.ddb_char_k.get()])
        _updateDdbHooks(Windows.ddb_char_v, _hooks, _cfg_json['ddb_char_v'])
        _hooks = list(Cfg.allHooks[Windows.ddb_content_k.get()])
        _updateDdbHooks(Windows.ddb_content_v, _hooks, _cfg_json['ddb_content_v'])


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
    # ===== 日志记录 =====
    label_log: tk.Label
    button_log: tk.Button
    button_log_control: tk.Button

    root = tk.Tk()


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.1 " + "管理员" if windows.IsUserAnAdmin() else "非管理员")  # 窗口名
Windows.root.geometry('640x320+10+10')  # axb为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
# Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

# ===== dll目录 =====
Windows.label_hook_dll_root = tk.Label(Windows.root)
Windows.label_hook_dll_root.grid(row=99, column=1, columnspan=4)
_set_hook_dll_root(_cfg_json['hook_dll_root'])


def button_hook_dll_root():
    _askd_hook_dll_root = tkf.askdirectory(
        title='LunaHost.dll的目录',
        initialdir=Cfg.hook_dll_root
    )
    if not _askd_hook_dll_root:
        return
    _cfg_json['hook_dll_root'] = _askd_hook_dll_root
    _set_hook_dll_root(_askd_hook_dll_root)


Windows.button_hook_dll_root = tk.Button(
    Windows.root,
    text='选择 LunaHook 目录',
    command=button_hook_dll_root
)
Windows.button_hook_dll_root.grid(row=99, column=0)

# ===== 日志记录 =====
Windows.label_log = tk.Label(Windows.root, text=_cfg_json['label_log'])
Windows.label_log.grid(row=100, column=1, columnspan=4)


def button_log():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _askd_path = tkf.asksaveasfilename(
        title='Log 路径',
        initialdir=_dir,
        initialfile=_file
    )
    if not _askd_path:
        return
    _cfg_json['label_log'] = os.path.abspath(_askd_path)
    Windows.label_log.config(text=_cfg_json['label_log'])


Windows.button_log = tk.Button(
    Windows.root,
    text='选择 Log 路径',
    command=button_log
)
Windows.button_log.grid(row=100, column=0)


def button_log_control():
    if not Cfg.log:
        Windows.button_log_control.config(text='暂停记录')
        Cfg.log_file = open(_cfg_json['label_log'], 'a', encoding='utf-8')
    else:
        Windows.button_log_control.config(text='继续记录')
        Cfg.log_file.close()
    Cfg.log = not Cfg.log


Windows.button_log_control = tk.Button(
    Windows.root,
    text='开始记录',
    command=button_log_control
)
Windows.button_log_control.grid(row=101, column=5)


def log_process():
    if (not Cfg.log) or not Cfg.var_d:
        return
    Cfg.log_add_size += Cfg.log_file.write(clearT(Cfg.var_n) + '：' + clearT(Cfg.var_d) + '\n')


# ===== 选择进程 =====
Windows.label_AttachProcessPID = tk.Label(Windows.root, text=f'等待注入进程')
Windows.label_AttachProcessPID.grid(row=0, column=1)


def ddb_encoding_list(_current=0):
    _ddb = ttk.Combobox(Windows.root)
    _ddb['value'] = Cfg.encoding_list
    _ddb.current(_current)
    return _ddb


Windows.ddb_AttachProcess_codepage = ddb_encoding_list(_cfg_json['ddb_AttachProcess_codepage'])
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
Windows.ddb_char = ddb_encoding_list(_cfg_json['ddb_char'])
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
Windows.ddb_content = ddb_encoding_list(_cfg_json['ddb_content'])
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
    _tmp = Cfg.hook.hookdatacollecter
    _hooks = {}
    for key in _tmp.keys():
        if key[4] not in _hooks:
            _hooks[key[4]] = {key[5]}
        else:
            _hooks[key[4]].add(key[5])
    print(_hooks)
    Cfg.allHooks = _hooks
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


def _cb_n():
    Windows.label_cb_n.config(text=Cfg.var_n)


def cb_n(key, output: str):
    if key[4] == Windows.ddb_char_k.get() and key[5] == Windows.ddb_char_v.get():
        if Windows.ddb_AttachProcess_codepage.get() != Windows.ddb_char.get():
            tmp = output.encode(
                Windows.ddb_AttachProcess_codepage.get(), errors='ignore'
            ).decode(Windows.ddb_char.get(), errors='ignore')
        else:
            tmp = output
        if not tmp:
            tmp = '旁白'
        if Cfg.var_n != tmp:
            Cfg.var_n = tmp
            Windows.root.after(1, _cb_n)


Cfg.callback_list.append(cb_n)

Windows.label_cb_d = tk.Label(Windows.root, text=f'内容')
Windows.label_cb_d.grid(row=98, columnspan=4, sticky=tk.W)


def _cb_d():
    Windows.label_cb_d.config(text=Cfg.var_d)


def cb_d(key, output):
    if key[4] == Windows.ddb_content_k.get() and key[5] == Windows.ddb_content_v.get():
        if Windows.ddb_AttachProcess_codepage.get() != Windows.ddb_content.get():
            tmp = output.encode(
                Windows.ddb_AttachProcess_codepage.get(), errors='ignore'
            ).decode(Windows.ddb_content.get(), errors='ignore')
        else:
            tmp = output
        if Cfg.var_d != tmp:
            Cfg.var_d = tmp
            Windows.root.after(10, log_process)
            Windows.root.after(20, _cb_d)


Cfg.callback_list.append(cb_d)


# ===== 时钟循环 =====
def clock_loop():
    if Cfg.hook is not None:
        _tmp = Cfg.hook.hookdatacollecter
        if _tmp:
            button_content()
            return
    Windows.root.after(500, clock_loop)


if not Cfg.allHooks:
    Windows.root.after(500, clock_loop)
else:
    updateAllHooks()


def log_flush():
    try:
        if (not Cfg.log) or not Cfg.var_d:
            return
        if Cfg.log_add_size > 0:
            Cfg.log_file.flush()
            Cfg.log_add_size = 0
    finally:
        Windows.root.after(2000, log_flush)


Windows.root.after(2000, log_flush)


# ===== 进入消息循环 =====
def on_closing():
    if Cfg.log:
        button_log()
    if messagebox.askokcancel("保存", "保存当前状态?"):
        _cfg_json['ddb_AttachProcess_codepage'] = Windows.ddb_AttachProcess_codepage.current()
        _cfg_json['ddb_char'] = Windows.ddb_char.current()
        _cfg_json['ddb_content'] = Windows.ddb_content.current()
        _cfg_json['allHooks'] = {k: list(v) for k, v in Cfg.allHooks.items()}
        _cfg_json['ddb_char_k'] = Windows.ddb_char_k.current()
        _cfg_json['ddb_char_v'] = Windows.ddb_char_v.current()
        _cfg_json['ddb_content_k'] = Windows.ddb_content_k.current()
        _cfg_json['ddb_content_v'] = Windows.ddb_content_v.current()
        # ===== 持久化设置 =====
        with open(r'config.json', 'w', encoding='utf-8') as f:
            json.dump(_cfg_json, f, ensure_ascii=False, indent=4)

    Windows.root.destroy()


Windows.root.protocol("WM_DELETE_WINDOW", on_closing)
Windows.root.mainloop()
