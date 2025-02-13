import subprocess
import sys
import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Dependencies required
REQUIRED_PACKAGES = [
    "fastapi", "uvicorn", "openai", "pillow", "pytesseract",
    "sentence-transformers", "sqlite3"
]

# Function to install missing dependencies
def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

install_missing_packages()

@app.get("/")
def read_root():
    return {"message": "Automation Agent is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
