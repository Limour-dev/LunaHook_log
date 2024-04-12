@echo off
:: 将控制台代码页更改为 UTF-8
chcp 65001 > nul
:: 运行程序
start "LunaHook" C:\Users\11248\miniconda3\envs\LunaHook_log\python.exe %1\main.py
:: 等待用户按任意键继续
pause