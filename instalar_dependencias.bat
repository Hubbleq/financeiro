@echo off
echo ========================================
echo  Instalando Dependencias do Projeto
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar o ambiente virtual
        echo Verifique se o Python esta instalado
        pause
        exit /b 1
    )
)

REM Ativar o ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para usar o sistema:
echo   1. Execute: ativar_ambiente.bat
echo   2. Execute: python exemplo_uso.py
echo   3. Ou execute: streamlit run dashboard_financeiro.py
echo.
pause
