@echo off
set MAVEN_PROJECTBASEDIR=%~dp0
set MAVEN_PROJECTBASEDIR=%MAVEN_PROJECTBASEDIR:~0,-1%
set JAVA_EXE=%JAVA_HOME%\bin\java.exe
if not exist "%JAVA_EXE%" set JAVA_EXE=java

"%JAVA_EXE%" -cp "%MAVEN_PROJECTBASEDIR%\.mvn\wrapper\maven-wrapper.jar" -Dmaven.multiModuleProjectDirectory="%MAVEN_PROJECTBASEDIR%" org.apache.maven.wrapper.MavenWrapperMain %*
@echo off
REM Minimal Maven wrapper (Windows) — downloads the Takari maven-wrapper jar if missing
setlocal
set SCRIPT_DIR=%~dp0
set WRAPPER_DIR=%SCRIPT_DIR%.mvn\wrapper
set JAR=%WRAPPER_DIR%\maven-wrapper.jar
set JAR_URL=https://repo1.maven.org/maven2/io/takari/maven-wrapper/0.5.6/maven-wrapper-0.5.6.jar

if not exist "%JAR%" (
  if exist "%WRAPPER_DIR%" ( ) else (mkdir "%WRAPPER_DIR%")
  powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%JAR_URL%','%JAR%')"
)

java -cp "%JAR%" -Dmaven.multiModuleProjectDirectory="%~dp0" org.apache.maven.wrapper.MavenWrapperMain %*
