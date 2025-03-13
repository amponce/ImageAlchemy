@echo off
:: cleanup.bat - Clean up temporary output folders for Windows

echo Cleaning up temporary output directories...

:: Remove all output folders
for /d %%i in (output_*) do rmdir /s /q "%%i"
for /d %%i in (tmp_*) do rmdir /s /q "%%i"

echo Cleanup complete!