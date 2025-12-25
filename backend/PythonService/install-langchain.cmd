@echo off
echo ========================================
echo Installing LangChain for AI Agent
echo ========================================
echo.

echo [1/4] Fixing anyio version conflict...
py -3.11 -m pip install --user "anyio<4.0.0,>=3.7.1" --force-reinstall

echo.
echo [2/4] Installing LangChain core...
py -3.11 -m pip install --user langchain>=0.1.0

echo.
echo [3/4] Installing LangChain Google Generative AI...
py -3.11 -m pip install --user langchain-google-genai>=0.0.6

echo.
echo [4/4] Installing LangChain Community (minimal)...
py -3.11 -m pip install --user langchain-community>=0.0.20 --no-deps
py -3.11 -m pip install --user langchain-core pydantic

echo.
echo ========================================
echo ✅ LangChain installation complete!
echo ========================================
echo.
echo Test installation:
py -3.11 -c "print('Testing...'); from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ LangChain OK')"

echo.
echo You can now use LangChain Agent!
echo Start service: python main.py
echo Test endpoint: POST http://localhost:8000/api/chat/langchain
pause
