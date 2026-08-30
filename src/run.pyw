import subprocess
from pathlib import Path

folder = Path(__file__).parent

subprocess.Popen([
    "python",
    str(folder / "main.py")
])