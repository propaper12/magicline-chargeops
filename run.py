"""
ChargeOps AI - Calistirma Scripti (Entrypoint)
Magicline Enerji Sistemleri Cozum Projesi
"""

import sys
import os
from pathlib import Path
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.chdir(str(BASE_DIR))

if __name__ == "__main__":
    print("=" * 70)
    print("[START] ChargeOps AI: Autonomous EV Charging Telemetry & Predictive Maintenance")
    print("[TARGET] Magicline Enerji Sistemleri Sanayi ve Ticaret Ltd. Sti.")
    print("[URL] http://127.0.0.1:8002")
    print("=" * 70)
    uvicorn.run("main:app", host="127.0.0.1", port=8002, app_dir=str(BASE_DIR))
