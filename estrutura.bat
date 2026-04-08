@echo off

rmdir /s /q installer\app
mkdir installer\app
mkdir installer\app\ffmpeg

copy dist\TranscriberPipeline.exe installer\app\
copy ffmpeg\ffmpeg.exe installer\app\ffmpeg\

echo Estrutura pronta para installer!
pause