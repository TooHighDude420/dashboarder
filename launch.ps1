if (Test-Path ".\venv" -PathType Container) {
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python .\main.py
} else {
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python .\main.py
}
