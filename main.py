import datetime
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import subprocess
import os
import json
import sqlite3
from pathlib import Path

app = FastAPI()
DATA_DIR = "/data"  # Directory where files are stored

# Helper function to execute shell commands
def run_shell(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Endpoint 1: Execute a task
@app.post("/run")
def run_task(task: str):
    try:
        if "install uv" in task:
            run_shell("pip install uv")
            run_shell(f"uv {DATA_DIR}/datagen.py {os.getenv('USER_EMAIL')}")
            return {"status": "success", "message": "Data generated."}

        elif "count wednesdays" in task:
            file_path = f"{DATA_DIR}/dates.txt"
            if not Path(file_path).exists():
                raise HTTPException(status_code=400, detail="File does not exist.")
            
            with open(file_path, "r") as f:
                dates = f.readlines()
            
            wednesday_count = sum(
                1 for date in dates if datetime.datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2
            )
            
            with open(f"{DATA_DIR}/dates-wednesdays.txt", "w") as f:
                f.write(str(wednesday_count))

            return {"status": "success", "message": f"Wednesdays counted: {wednesday_count}"}

        else:
            raise HTTPException(status_code=400, detail="Task not recognized.")

    except HTTPException as e:
        raise e  # Forward known errors with proper status codes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle unexpected errors

# ✅ Endpoint 2: Read a file's content
@app.get("/read")
def read_file(path: str):
    try:
        file_path = Path(DATA_DIR) / path  # Ensure it's within the data directory

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found.")

        with open(file_path, "r") as f:
            content = f.read()

        return {"status": "success", "content": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
