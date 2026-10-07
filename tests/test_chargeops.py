"""
ChargeOps AI - Unit & Integration Test Suite
Magicline Enerji Sistemleri EV Sarj Telemetri ve Kestirimci Bakim Dogrulama Testleri
"""

import unittest
from fastapi.testclient import TestClient
from main import app
from database.connection import get_db_connection
from engines.predictive_engine import PredictiveMaintenanceEngine
from engines.forecasting_engine import DemandForecastingEngine

class TestChargeOpsAI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.pred_engine = PredictiveMaintenanceEngine()
        self.fore_engine = DemandForecastingEngine()

    def test_database_populated(self):
        """DuckDB Lakehouse tablolarinin ve gercekci verilerin varligini dogrular."""
        con = get_db_connection()
        try:
            stations = con.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
            sessions = con.execute("SELECT COUNT(*) FROM charging_sessions").fetchone()[0]
            logs = con.execute("SELECT COUNT(*) FROM telemetry_logs").fetchone()[0]

            self.assertGreaterEqual(stations, 6)
            self.assertGreaterEqual(sessions, 1000)
            self.assertGreaterEqual(logs, 5000)
        finally:
            con.close()

    def test_predictive_anomaly_detection(self):
        """Asiri isinma ve voltaj anomalilerinin dogru yakalandigini test eder."""
        diag = self.pred_engine.run_fleet_diagnostic()
        self.assertGreater(diag["overview"]["critical_alerts"], 0)
        
        # Maslak istasyonundaki termal asiri isinma yakalandi mi?
        maslak = next(s for s in diag["stations"] if s["station_id"] == "ML-IST-002")
        anomaly_types = [a["type"] for a in maslak["anomalies"]]
        self.assertIn("THERMAL_OVERHEAT_RISK", anomaly_types)

        # Kadikoy istasyonundaki sebeke voltaj dususu yakalandi mi?
        kadikoy = next(s for s in diag["stations"] if s["station_id"] == "ML-IST-003")
        anomaly_types_k = [a["type"] for a in kadikoy["anomalies"]]
        self.assertIn("GRID_UNDERVOLTAGE", anomaly_types_k)

    def test_demand_forecasting(self):
        """24 saatlik sebeke yuk egrisi ve pik saat modelini test eder."""
        profile = self.fore_engine.get_24h_load_profile()
        self.assertIn("peak_hours", profile)
        self.assertGreater(profile["peak_demand_kwh"], 0)

        rankings = self.fore_engine.get_station_performance_rankings()
        self.assertGreater(len(rankings["rankings"]), 0)

    def test_fastapi_endpoints(self):
        """FastAPI REST API rotalarinin 200 OK dondugunu dogrular."""
        r1 = self.client.get("/api/status")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["status"], "ONLINE")

        r2 = self.client.get("/api/fleet/kpis")
        self.assertEqual(r2.status_code, 200)
        self.assertGreater(r2.json()["total_revenue_tl"], 0)

        r3 = self.client.get("/api/fleet/diagnostics")
        self.assertEqual(r3.status_code, 200)

        r4 = self.client.get("/")
        self.assertEqual(r4.status_code, 200)

if __name__ == "__main__":
    unittest.main()
