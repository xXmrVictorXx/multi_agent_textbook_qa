@echo off
chcp 65001 >nul
echo ================================
echo 创建 .env 配置文件
echo ================================
echo.

echo 请选择要使用的API服务：
echo 1. 阿里云通义千问（推荐）
echo 2. DeepSeek（最便宜）
echo 3. 智谱AI GLM
echo.

set /p choice=请输入选项 (1/2/3): 

if "%choice%"=="1" goto dashscope
if "%choice%"=="2" goto deepseek
if "%choice%"=="3" goto zhipu

echo 无效选项，退出
pause
exit

:dashscope
echo.
echo 你选择了：阿里云通义千问
echo 请访问 https://dashscope.console.aliyun.com/ 获取API Key
echo.
set /p apikey=请输入你的API Key: 

(
echo OPENAI_API_KEY=%apikey%
echo OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
echo MODEL_NAME=qwen-turbo
) > .env

echo.
echo ✓ .env 文件创建成功！
echo 配置内容：
type .env
goto end

:deepseek
echo.
echo 你选择了：DeepSeek
echo 请访问 https://platform.deepseek.com/ 获取API Key
echo.
set /p apikey=请输入你的API Key: 

(
echo OPENAI_API_KEY=%apikey%
echo OPENAI_BASE_URL=https://api.deepseek.com
echo MODEL_NAME=deepseek-chat
) > .env

echo.
echo ✓ .env 文件创建成功！
echo 配置内容：
type .env
goto end

:zhipu
echo.
echo 你选择了：智谱AI GLM
echo 请访问 https://open.bigmodel.cn/ 获取API Key
echo.
set /p apikey=请输入你的API Key: 

(
echo OPENAI_API_KEY=%apikey%
echo OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
echo MODEL_NAME=glm-4
) > .env

echo.
echo ✓ .env 文件创建成功！
echo 配置内容：
type .env
goto end

:end
echo.
echo ================================
echo 配置完成！
echo ================================
echo.
echo 现在可以运行程序了：
echo   python main.py
echo.
pause

