@echo off
echo ========================================
echo  Ativando Ambiente Virtual Python
echo ========================================
echo.

REM Ativar o ambiente virtual
call .venv\Scripts\activate.bat

echo.
echo Ambiente virtual ativado com sucesso!
echo.
echo Comandos disponiveis:
echo   python exemplo_uso.py          - Executar exemplo
echo   streamlit run dashboard_financeiro.py  - Abrir dashboard
echo.
echo Para desativar o ambiente: deactivate
echo ========================================
