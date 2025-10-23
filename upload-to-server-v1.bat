@echo off

REM SSH KEY NEEDS TO BE CONFIGURED CORRECTLY

REM ======= CONFIGURATION =======
set LOCAL_FOLDER=assignments
set SERVER=scirouter.cslab.ece.ntua.gr
set REMOTE_FOLDER=~/assignments-upload
REM ============================

echo Deleting files on server...
ssh %SERVER% "rm -rf %REMOTE_FOLDER%/%LOCAL_FOLDER%/*"

echo Uploading current files to server...
scp -r "%~dp0%LOCAL_FOLDER%" %SERVER%:%REMOTE_FOLDER%