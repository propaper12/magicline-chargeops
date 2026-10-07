"""
ChargeOps AI - Sentetik OCPP Telemetri & Seans Veri Ureticisi
Magicline Enerji istasyon agini (DC 180kW, 120kW, 60kW ve AC 22kW) ve
kestirimci bakim anomalilerini (asiri isinma, voltaj dengesizligi) gercekci sekilde modeller.
"""

import random
from datetime import datetime, timedelta
from database.connection import get_db_connection
from config import TARIFF_CONFIG

def seed_chargeops_lakehouse(num_sessions: int = 1200, num_telemetry_samples: int = 8000):
    con = get_db_connection()
    print("[Seed Engine] DuckDB Lakehouse tablolari hazirlaniyor...")

    # 1. Tablolari olustur
    con.execute("DROP TABLE IF EXISTS telemetry_logs;")
    con.execute("DROP TABLE IF EXISTS charging_sessions;")
    con.execute("DROP TABLE IF EXISTS connectors;")
    con.execute("DROP TABLE IF EXISTS stations;")
    con.execute("DROP TABLE IF EXISTS maintenance_tickets;")

    con.execute("""
        CREATE TABLE stations (
            station_id VARCHAR PRIMARY KEY,
            station_name VARCHAR,
            city VARCHAR,
            district VARCHAR,
            station_type VARCHAR,
            total_connectors INTEGER,
            max_power_kw DOUBLE,
            installation_date TIMESTAMP,
            firmware_version VARCHAR,
            current_status VARCHAR
        );
    """)

    con.execute("""
        CREATE TABLE connectors (
            connector_id VARCHAR PRIMARY KEY,
            station_id VARCHAR,
            connector_number INTEGER,
            connector_type VARCHAR,
            max_power_kw DOUBLE,
            status VARCHAR
        );
    """)

    con.execute("""
        CREATE TABLE charging_sessions (
            session_id VARCHAR PRIMARY KEY,
            station_id VARCHAR,
            connector_id VARCHAR,
            user_rfid_or_app_id VARCHAR,
            energy_delivered_kwh DOUBLE,
            total_price_tl DOUBLE,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            duration_minutes INTEGER,
            initial_soc INTEGER,
            final_soc INTEGER,
            stop_reason VARCHAR
        );
    """)

    con.execute("""
        CREATE TABLE telemetry_logs (
            log_id VARCHAR PRIMARY KEY,
            station_id VARCHAR,
            connector_id VARCHAR,
            voltage_v DOUBLE,
            current_a DOUBLE,
            active_power_kw DOUBLE,
            cable_temperature_c DOUBLE,
            soc_pct INTEGER,
            error_code VARCHAR,
            timestamp TIMESTAMP
        );
    """)

    con.execute("""
        CREATE TABLE maintenance_tickets (
            ticket_id VARCHAR PRIMARY KEY,
            station_id VARCHAR,
            connector_id VARCHAR,
            anomaly_type VARCHAR,
            severity VARCHAR,
            predicted_failure_hours INTEGER,
            details VARCHAR,
            recommended_action VARCHAR,
            created_at TIMESTAMP,
            status VARCHAR
        );
    """)

    # 2. Istasyonlari Ekle
    print("[Seed Engine] 1. 'stations' ve 'connectors' tablolari dolduruluyor...")
    station_configs = [
        ("ML-IST-001", "Magicline Tekstilkent Merkez DC Ultra", "İstanbul", "Esenler", "DC_ULTRA", 2, 180.0, "v2.5.1", "Available"),
        ("ML-IST-002", "Magicline Maslak Plazalar DC Hızlı", "İstanbul", "Sarıyer", "DC_FAST", 2, 120.0, "v2.4.8", "Charging"),
        ("ML-IST-003", "Magicline Kadıköy Rıhtım Hibrit İstasyon", "İstanbul", "Kadıköy", "DC_FAST", 2, 60.0, "v2.4.2", "Charging"),
        ("ML-IST-004", "Magicline Ataşehir Finans Merkezi DC", "İstanbul", "Ataşehir", "DC_FAST", 2, 120.0, "v2.5.0", "Available"),
        ("ML-KOC-005", "Magicline Gebze Otoyol Dinlenme DC Ultra", "Kocaeli", "Gebze", "DC_ULTRA", 2, 180.0, "v2.5.1", "Available"),
        ("ML-BUR-006", "Magicline Nilüfer AVM AC Akıllı Şarj", "Bursa", "Nilüfer", "AC_NORMAL", 2, 22.0, "v1.9.4", "Available")
    ]

    connectors_list = []
    for sid, sname, city, dist, stype, conns, max_p, fw, status in station_configs:
        inst_date = datetime.now() - timedelta(days=random.randint(120, 600))
        con.execute("""
            INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [sid, sname, city, dist, stype, conns, max_p, inst_date, fw, status])

        for c_idx in range(1, conns + 1):
            cid = f"{sid}-C{c_idx}"
            ctype = "CCS2" if "DC" in stype else "Type2"
            p_cap = max_p / conns if "DC" in stype else max_p
            c_status = "Available" if random.random() > 0.4 else "Charging"
            con.execute("""
                INSERT INTO connectors VALUES (?, ?, ?, ?, ?, ?)
            """, [cid, sid, c_idx, ctype, p_cap, c_status])
            connectors_list.append((cid, sid, stype, p_cap))

    # 3. Gercekci Seans Verileri Uretimi
    print("[Seed Engine] 2. 'charging_sessions' tablosu (1200 seans) uretiliyor...")
    stop_reasons = ["EVDisconnected", "LocalStop", "EmergencyStop", "RemoteStop"]
    session_ids = []

    now = datetime.now()
    for s_idx in range(1, num_sessions + 1):
        sess_id = f"SES-{10000 + s_idx}"
        cid, sid, stype, p_cap = random.choice(connectors_list)
        
        # Son 90 gun icinde rastgele seans zamanlari
        days_ago = random.randint(0, 90)
        # Gun icinde saat agirliklari (Pik saatler 17:00 - 21:00 arasi daha yogun)
        hour = random.choices(
            list(range(24)),
            weights=[1, 1, 1, 1, 1, 2, 4, 6, 7, 6, 5, 5, 6, 6, 7, 8, 10, 12, 11, 9, 7, 5, 3, 2]
        )[0]
        minute = random.randint(0, 59)
        start_time = (now - timedelta(days=days_ago)).replace(hour=hour, minute=minute, second=0)

        initial_soc = random.randint(10, 45)
        target_soc = random.randint(min(80, initial_soc + 20), 98)
        soc_diff = target_soc - initial_soc

        if "DC" in stype:
            duration = random.randint(22, 55) # 22 - 55 dakika
            # 60kWh batarya bazinda yaklasik sarj edilen enerji
            energy_kwh = round((soc_diff / 100.0) * random.uniform(50.0, 75.0), 2)
            price_tl = round(energy_kwh * TARIFF_CONFIG["dc_price_per_kwh"], 2)
        else:
            duration = random.randint(90, 240) # AC daha yavas
            energy_kwh = round(min(22.0, (duration / 60.0) * 11.0), 2)
            price_tl = round(energy_kwh * TARIFF_CONFIG["ac_price_per_kwh"], 2)

        end_time = start_time + timedelta(minutes=duration)
        stop_reason = random.choices(stop_reasons, weights=[0.82, 0.12, 0.04, 0.02])[0]
        user_id = f"USR-TR{random.randint(1000, 9999)}"

        con.execute("""
            INSERT INTO charging_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [sess_id, sid, cid, user_id, energy_kwh, price_tl, start_time, end_time, duration, initial_soc, target_soc, stop_reason])
        session_ids.append((sess_id, sid, cid, start_time, end_time, stype))

    # 4. Telemetri Loglari (OCPP MeterValues Akisi)
    print("[Seed Engine] 3. 'telemetry_logs' (8000+ satır telemetri ve planlı anomaliler) uretiliyor...")
    
    # 8.000 log kaydı
    for l_idx in range(1, num_telemetry_samples + 1):
        log_id = f"TLM-{100000 + l_idx}"
        cid, sid, stype, p_cap = random.choice(connectors_list)
        
        # Son 14 gun icindeki telemetri akisi
        t_minutes_ago = random.randint(0, 14 * 24 * 60)
        t_time = now - timedelta(minutes=t_minutes_ago)

        # Standart normal parametreler
        voltage = round(random.gauss(230.0, 3.5), 1)
        cable_temp = round(random.gauss(38.0, 5.0), 1)
        err_code = "NoError"

        if "DC" in stype:
            power = round(random.uniform(35.0, min(140.0, p_cap)), 1)
            current = round((power * 1000.0) / (voltage * 1.732), 1) # 3 Faz DC besleme
            cable_temp += random.uniform(8.0, 15.0) # DC sarj daha cok isitir
        else:
            power = round(random.uniform(7.0, 22.0), 1)
            current = round((power * 1000.0) / voltage, 1)

        soc = random.randint(20, 90)

        # PLANLI KESTIRIMCI BAKIM ANOMALILERI (Predictive Maintenance Anomaly Injection)
        # Senaryo A: Maslak ML-IST-002-C2 soketi son 48 saatte asiri isiniyor (Thermal Overheat Anomaly)
        if sid == "ML-IST-002" and cid == "ML-IST-002-C2" and t_minutes_ago < (48 * 60):
            cable_temp = round(random.uniform(62.0, 74.5), 1) # 68°C kritik esigini asar
            if cable_temp > 70.0:
                err_code = "OverTemperatureWarning"

        # Senaryo B: Kadikoy ML-IST-003 istasyonunda sebeke voltaji dusuk ve dengesiz (Grid Voltage Drop)
        if sid == "ML-IST-003" and t_minutes_ago < (72 * 60):
            voltage = round(random.uniform(198.0, 206.5), 1) # 207V altina duser
            if voltage < 203.0:
                err_code = "UnderVoltageAlert"

        con.execute("""
            INSERT INTO telemetry_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [log_id, sid, cid, voltage, current, power, cable_temp, soc, err_code, t_time])

    con.close()
    print("[Seed Engine] [SUCCESS] DuckDB Lakehouse basariyla olusturuldu:")
    print(f"    * stations: {len(station_configs)} sarj istasyonu")
    print(f"    * connectors: {len(connectors_list)} soket")
    print(f"    * charging_sessions: {num_sessions} seans kaydi")
    print(f"    * telemetry_logs: {num_telemetry_samples} OCPP telemetri logu")

if __name__ == "__main__":
    seed_chargeops_lakehouse()
