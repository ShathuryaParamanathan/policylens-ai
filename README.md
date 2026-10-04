# policylens-ai
activate 
.\.venv\Scripts\Activate.ps1
deactivate
deactivate
run
uvicorn backend.app.main:app --reload