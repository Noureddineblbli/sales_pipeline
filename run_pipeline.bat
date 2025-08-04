@echo off
ECHO --- [%date% %time%] Starting Pipeline Run ---

REM The command 'CALL' is used to run another batch file and then return here.
REM The variable '%~dp0' automatically expands to the directory where this batch file is located.
ECHO Activating virtual environment...
CALL "%~dp0\venv\Scripts\activate.bat"

REM Step 1: Generate new daily data
ECHO.
ECHO --- [%date% %time%] Running Data Generator ---
python "%~dp0\generate_data.py"

REM Step 2: Run the main ETL process
ECHO.
ECHO --- [%date% %time%] Running ETL Script ---
python "%~dp0\etl.py"

REM Step 3: Generate the final report
ECHO.
ECHO --- [%date% %time%] Running Report Generator ---
python "%~dp0\report.py"

ECHO.
ECHO --- [%date% %time%] Pipeline Run Finished ---

REM Deactivate the virtual environment (good practice)
CALL "%~dp0\venv\Scripts\deactivate.bat"