@echo off
REM Runa Development Batch Script
REM Provides convenient commands for development, testing, and maintenance

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="test" goto test
if "%1"=="test-lexer" goto test-lexer
if "%1"=="test-parser" goto test-parser
if "%1"=="demo" goto demo
if "%1"=="install" goto install
if "%1"=="clean" goto clean

:help
echo Runa Development Commands:
echo.
echo   runa-dev test         - Run all tests (lexer + parser)
echo   runa-dev test-lexer   - Run only lexer tests
echo   runa-dev test-parser  - Run only parser tests
echo   runa-dev demo         - Run comprehensive parser demonstration
echo   runa-dev install      - Install Runa in development mode
echo   runa-dev clean        - Clean temporary files
echo.
goto end

:test
echo Running all Runa tests...
python -m pytest runa/tests/ -v
goto end

:test-lexer
echo Running lexer tests...
python -m pytest runa/tests/test_lexer.py -v
goto end

:test-parser
echo Running parser tests...
python -m pytest runa/tests/test_parser.py -v
goto end

:demo
echo 🚀 Running Runa Parser Demonstration...
python -c "from runa.compiler import parse_runa_source; from collections import Counter; source = open('runa/examples/parser_demo.runa').read(); program = parse_runa_source(source); print(f'✅ Parsed {len(program.statements)} statements'); types = [type(s).__name__ for s in program.statements]; counts = Counter(types); print('Statement types:'); [print(f'  {t}: {c}') for t, c in sorted(counts.items())]"
goto end

:install
echo Installing Runa in development mode...
pip install -e .
goto end

:clean
echo Cleaning temporary files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"
goto end

:end 