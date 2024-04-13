# LunaHook_log
+ Galgame游玩记录器，记录与纸片人的一点一滴

![e407cbf484c974c3e4aa3b8e9775cbf](https://github.com/Limour-dev/LunaHook_log/assets/93720049/904e4827-85de-450d-bb7f-e261305a9775)

## 安装
### 第一步 下载 LunaHook
+ https://github.com/HIllya51/LunaHook/releases
### 第二步 下载本仓库
+ https://github.com/Limour-dev/LunaHook_log/archive/refs/heads/main.zip
### 第三步 安装 python
+ https://www.python.org/
### 第四步 安装依赖
+ `pip install OpenCC -i https://pypi.tuna.tsinghua.edu.cn/simple some-package`
### 附加 安装 PsExec64
+ https://learn.microsoft.com/en-us/sysinternals/downloads/psexec
+ 将 `PsExec64.exe` 放到与 `main.py` 相同的目录
### 第五步 修改 bat脚本 中 python 的路径
+ 用记事本打开 `RunPy.bat` , 将 python 路径改成自己安装的 python 路径

## 使用
### 第零步 启动游戏
+ 先用低权限运行要记录的游戏
### 第一步 启动记录器
+ 至少使用管理员权限的 `RunAsAdmin.bat`，双击启动。
+ 执行了附加的安装步骤的话，双击 `RunAsSystem.bat` 可以以更高的权限运行，避免检测
### 第二步 选择 LunaHook 路径
+ 点击 `选择 LunaHook 目录`，选择 LunaHook 所在的目录
### 第三步 注入进程
+ 在 `注入进程` 一行选择合适的编码，点击 `注入进程` 后，选择所启动的游戏
### 第四步 获取钩子
+ 开始游戏，直到控制台输出钩子的信息
+ 此时点击 `更新钩子列表`
+ 第一个对应人名，第二个对应对白，分别选择合适的编码和相应的钩子
### 第五步 开始记录
+ 点击 `选择 Log 目录`，选择要将记录保存到哪里
+ 点击 `开始记录`，游玩游戏，过一段时间看看记录有没有成功保存
### 第六步 关闭记录器
+ 关闭记录器时会询问是否保存当前界面的配置
+ 如果保存后想重置，删除目录中的 `config.json` 即可
## 翻译
+ https://github.com/Limour-dev/SakuraTrans
