@echo off

REM Requirements
REM Server A: "assignments" folder in home directory
REM Server B: "assignments-upload/assignments" folder in home directory

REM ======= CONFIGURATION =======
set LOCAL_FOLDER=%~dp0assignments
set SERVER_A=parlab48@orion.cslab.ece.ntua.gr
set REMOTE_FOLDER=~
set SERVER_B=scirouter.cslab.ece.ntua.gr
set REMOTE_FOLDER_B=~/assignments-upload
REM ============================

echo Upload to Orion server
scp -r "%LOCAL_FOLDER%" %SERVER_A%:%REMOTE_FOLDER%

echo Upload from Orion to Scirouter server
ssh %SERVER_A% "scp -r %REMOTE_FOLDER%/assignments %SERVER_B%:%REMOTE_FOLDER_B%"

echo COMPLETED

pause