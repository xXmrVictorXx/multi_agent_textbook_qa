@echo off
echo Starting Steampunk TextbookQA Server...
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
pause
