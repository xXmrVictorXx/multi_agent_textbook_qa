@echo off
chcp 65001 >nul
echo ================================
echo 创建 .env 配置文件
echo ================================
echo.

echo.
echo 使用OpenAI-Python接口访问LLM
echo 请输入Base URL:
echo 参考:
echo    OpenAI: https://api.openai.com/v1
echo    阿里云: https://dashscope.aliyuncs.com/compatible-mode/v1
echo    DeepSeek: https://api.deepseek.com/chat/completions
echo    智谱AI: https://open.bigmodel.cn/api/paas/v4/
echo    OpenRouter: https://openrouter.ai/api/v1
echo    Ollama: http://localhost:11434/v1
echo.
set /p baseurl=^>
echo.
echo 请输入API Key:
set /p apikey=^>
echo.
echo 请输入模型名称
set /p modelname=^>

(
echo OPENAI_API_KEY=%apikey%
echo OPENAI_BASE_URL=%baseurl%
echo MODEL_NAME=%modelname%
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

