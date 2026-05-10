@echo off
echo Booting up the Circuit Master Pro Engine...
cd /d "%~dp0"
call streamlit run app.py
pause