@echo off
chcp 65001 >nul
@echo off
setlocal enabledelayedexpansion
title SNEERYBOOSTER V1 - Download ^& Install
color 0B

echo ============================================
echo   SNEERYBOOSTER V1 - Download ^& Install
echo   White Frosted Gaming Control Center
echo ============================================
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    echo Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

:: Ensure Microsoft Edge WebView2 runtime (Tauri needs it to render the UI)
echo [PRE] Ensuring Microsoft Edge WebView2 runtime...
set "WV_FOUND=0"
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A08C11}" >nul 2>nul && set "WV_FOUND=1"
reg query "HKCU\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A08C11}" >nul 2>nul && set "WV_FOUND=1"
if "%WV_FOUND%"=="1" (
    echo [INFO] WebView2 runtime already present.
) else (
    echo [INFO] WebView2 not found - downloading runtime installer...
    set "WV_URL=https://go.microsoft.com/fwlink/?LinkId=2198023"
    set "WV_SETUP=%TEMP%\MicrosoftEdgeWebview2Setup.exe"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri '%WV_URL%' -OutFile '%WV_SETUP%' -UseBasicParsing; exit 0 } catch { Write-Error $_; exit 1 }"
    if %errorlevel% neq 0 (
        echo [WARN] Could not download WebView2 runtime. The app may fail to open.
    ) else (
        echo [INFO] Installing WebView2 runtime (silent)...
        start /wait "" "%WV_SETUP%" --silent --install
        echo [INFO] WebView2 runtime install finished.
    )
)

:: Setup paths (all quoted to survive spaces in folder name)
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
set "EXE_NAME=SNEERYBOOSTER_V1.exe"
set "EXE_URL=https://github.com/thanhtu170585-dev/Zenith-booster/releases/latest/download/SNEERYBOOSTER_V1.exe"
set "DEST_DIR=%ROOT%"
set "DEST_EXE=%DEST_DIR%\%EXE_NAME%"

echo [1/4] Checking for existing installation...
if exist "%DEST_EXE%" (
    echo [INFO] Found existing %EXE_NAME%
    echo [INFO] Backing up current version...
    for /f "delims=" %%I in ('powershell -NoProfile -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set timestamp=%%I
    set timestamp=!datetime:~0,8!_!datetime:~8,6!
    if exist "%DEST_DIR%\SNEERYBOOSTER_V1_backup_!timestamp!.exe" del /f /q "%DEST_DIR%\SNEERYBOOSTER_V1_backup_!timestamp!.exe" >nul 2>nul
    move /y "%DEST_EXE%" "%DEST_DIR%\SNEERYBOOSTER_V1_backup_!timestamp!.exe" >nul 2>nul
    if !errorlevel! equ 0 (
        echo [INFO] Backed up to SNEERYBOOSTER_V1_backup_!timestamp!.exe
    ) else (
        echo [WARN] Could not backup - will overwrite
        del /f /q "%DEST_EXE%" >nul 2>nul
    )
)

echo [2/4] Downloading latest version...
echo [INFO] Downloading from: %EXE_URL%
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri '%EXE_URL%' -OutFile '%DEST_EXE%' -UseBasicParsing; exit 0 } catch { Write-Error $_; exit 1 }"
if %errorlevel% neq 0 (
    echo [ERROR] Download failed. Check your internet connection.
    echo [HINT] You can also download manually from: %EXE_URL%
    pause
    exit /b 1
)
echo [INFO] Download complete.

echo [3/4] Verifying download...
if not exist "%DEST_EXE%" (
    echo [ERROR] Downloaded file not found!
    pause
    exit /b 1
)
for %%I in ("%DEST_EXE%") do set FILESIZE=%%~zI
if %FILESIZE% LSS 5000000 (
    echo [WARN] File seems small (%FILESIZE% bytes). Download may be incomplete.
)
echo [INFO] File size: %FILESIZE% bytes

echo [4/4] Verifying executable...
:: Check if it's a valid PE executable (MZ header 0x4D 0x5A)
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $bytes = [System.IO.File]::ReadAllBytes('%DEST_EXE%'); if ($bytes.Length -ge 2 -and $bytes[0] -eq 0x4D -and $bytes[1] -eq 0x5A) { Write-Host '[INFO] Valid PE executable (MZ header found)'; exit 0 } else { Write-Host '[ERROR] Not a valid PE executable'; exit 1 } } catch { Write-Host 'Error: ' $_; exit 1 }"
if %errorlevel% neq 0 (
    echo [ERROR] Downloaded file is not a valid executable!
    del /f /q "%DEST_EXE%" >nul 2>nul
    pause
    exit /b 1
)
echo [INFO] Executable verified successfully.

echo.
echo ============================================
echo   INSTALLATION COMPLETE!
echo ============================================
echo.
echo [INFO] Installed to: %DEST_EXE%
echo [INFO] File size: %FILESIZE% bytes
echo.
echo You can now run SNEERYBOOSTER V2 by double-clicking:
echo %DEST_EXE%
echo.
echo [TIP] Right-click the exe and select "Run as administrator"
echo       for full optimization features.
echo.
echo ============================================
pause
