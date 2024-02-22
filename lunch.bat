@echo off
setlocal enabledelayedexpansion

REM 检查并安装依赖包
set "dependencies=flask flask-socketio"

for %%i in (%dependencies%) do (
    python -m pip show %%i > nul 2>&1
    if errorlevel 1 (
        echo Installing %%i...
        python -m pip install %%i
    ) else (
        echo %%i is already installed.
    )
)

REM 运行 lunch.py 文件
REM ...

echo Dependencies installation completed.
