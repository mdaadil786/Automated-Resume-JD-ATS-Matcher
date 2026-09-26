import subprocess
import sys
from app.config import settings

subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    "frontend/streamlit_app.py",
    "--server.port", str(settings.STREAMLIT_PORT)
], check=True)
