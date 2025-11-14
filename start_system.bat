@echo off
REM BTP Multi-Agent System Startup Script for Windows
REM Usage: start_system.bat

echo ====================================================
echo     BTP Multi-Agent Construction Management
echo ====================================================
echo.

REM Create logs directory
if not exist logs mkdir logs

REM Start AgentArchitect
echo [1/5] Starting AgentArchitect on port 10005...
cd backend\AgentArchitecte
start /B python main.py --port 10005 > ..\..\logs\AgentArchitect.log 2>&1
cd ..\..
timeout /t 3 >nul

REM Start AgentCostEstimator
echo [2/5] Starting AgentCostEstimator on port 10004...
cd backend\AgentCoutEstimateur
start /B python main.py --port 10004 > ..\..\logs\AgentCostEstimator.log 2>&1
cd ..\..
timeout /t 3 >nul

REM Start AgentPlanning
echo [3/5] Starting AgentPlanning on port 10006...
cd backend\AgentPlanning
start /B python main.py --port 10006 > ..\..\logs\AgentPlanning.log 2>&1
cd ..\..
timeout /t 3 >nul

echo.
echo Waiting for agent initialization...
timeout /t 10 >nul

REM Start Host Agent
echo [4/5] Starting Host Agent on port 13000...
cd frontend\hostAgentAPI
start /B python api.py > ..\..\logs\host_agent.log 2>&1
cd ..\..
timeout /t 5 >nul

REM Start Frontend
echo [5/5] Starting Frontend on port 5174...
cd frontend\multiagent_front
start /B npm run dev > ..\..\logs\frontend.log 2>&1
cd ..\..
timeout /t 8 >nul

echo.
echo ====================================================
echo     System started successfully!
echo ====================================================
echo.
echo Active services:
echo   - AgentArchitect      : http://localhost:10005
echo   - AgentCostEstimator  : http://localhost:10004
echo   - AgentPlanning       : http://localhost:10006
echo   - Host Agent          : http://localhost:13000
echo   - Frontend            : http://localhost:5174
echo.
echo Logs available in: logs\
echo.
echo Open your browser: http://localhost:5174
echo.
echo Press Ctrl+C to stop or close this window
echo ====================================================
pause
