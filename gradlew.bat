
@echo off
if exist "%~dp0\gradle\wrapper\gradle-wrapper.jar" (
  java -jar "%~dp0\gradle\wrapper\gradle-wrapper.jar" %*
) else (
  echo Wrapper JAR missing; using system 'gradle' instead...
  gradle %*
)
