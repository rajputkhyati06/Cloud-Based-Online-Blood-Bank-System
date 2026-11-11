@echo off
title Cloud Blood Bank & Emergency Triage System - Launcher
color 0A
cls
echo ======================================================================
echo    CLOUD-BASED ONLINE BLOOD BANK ^& EMERGENCY TRIAGE SYSTEM
echo ======================================================================
echo.
echo [1/2] Starting Local Cloud Web Server on Port 5000...
echo [2/2] Opening your Web Browser automatically...
echo.
echo ----------------------------------------------------------------------
echo Access URL: http://127.0.0.1:5000
echo Quick Logins:
echo   - Admin:    admin@bloodbank.org    /  admin123
echo   - Hospital: emergency@apollohospitals.com  /  apollo123
echo   - Donor:    rahul.donor@gmail.com  /  donor123
echo ----------------------------------------------------------------------
echo.
echo Note: Is black window ko band mat karna jab tak Sir ko demo de rahe ho!
echo.

start "" "http://127.0.0.1:5000"
python app.py

pause
