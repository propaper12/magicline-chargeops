"""
ChargeOps AI - FastAPI Application Server
Magicline Enerji Sistemleri Icin Otonom EV Sarj Telemetri ve Kestirimci Bakim Servisi.
"""

import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from config import APP_NAME, APP_SUBTITLE, APP_VERSION, COMPANY_TARGET
from engines.predictive_engine import PredictiveMaintenanceEngine
from engines.forecasting_engine import DemandForecastingEngine
from database.connection import get_db_connection

app = FastAPI(
    title=APP_NAME,
    description=APP_SUBTITLE,
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictive_engine = PredictiveMaintenanceEngine()
forecasting_engine = DemandForecastingEngine()

@app.get("/api/status")
def get_status():
    return {
        "app_name": APP_NAME,
        "subtitle": APP_SUBTITLE,
        "version": APP_VERSION,
        "target_company": COMPANY_TARGET,
        "status": "ONLINE",
        "supported_protocols": ["OCPP 1.6J", "OCPP 2.0.1", "ISO 15118 (Plug & Charge)"]
    }

@app.get("/api/fleet/kpis")
def get_fleet_kpis():
    try:
        return forecasting_engine.get_cpo_summary_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fleet/diagnostics")
def get_fleet_diagnostics():
    try:
        return predictive_engine.run_fleet_diagnostic()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fleet/load-profile")
def get_fleet_load_profile():
    try:
        return forecasting_engine.get_24h_load_profile()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fleet/rankings")
def get_fleet_rankings():
    try:
        return forecasting_engine.get_station_performance_rankings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tickets/resolve/{ticket_id}")
def resolve_ticket(ticket_id: str):
    con = get_db_connection()
    try:
        con.execute("UPDATE maintenance_tickets SET status = 'RESOLVED' WHERE ticket_id = ?", [ticket_id])
        return {"success": True, "ticket_id": ticket_id, "status": "RESOLVED"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

# Frontend Statik Dizin
web_dir = Path(__file__).resolve().parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(str(web_dir / "index.html"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=False)
