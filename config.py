import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "chargeops_warehouse.duckdb")

APP_NAME = "ChargeOps AI"
APP_SUBTITLE = "Autonomous EV Charging Telemetry, Predictive Maintenance & Grid Load Intelligence"
APP_VERSION = "1.0.0"
COMPANY_TARGET = "Magicline Enerji Sistemleri Sanayi ve Ticaret Ltd. Şti."

# EPDK & CPO Fiyatlandirma ve Tarife Ayarlari (TL/kWh)
TARIFF_CONFIG = {
    "ac_price_per_kwh": 7.50,    # AC 22kW soket tarifesi (TL/kWh)
    "dc_price_per_kwh": 9.80,    # DC 60kW - 180kW hızlı şarj tarifesi (TL/kWh)
    "currency": "TL",
}

# Kestirimci Bakim ve OCPP Telemetri Esikleri (Predictive Maintenance Thresholds)
PREDICTIVE_THRESHOLDS = {
    # Sicaklik Esikleri (CCS2 / Type2 Kablo & Soket)
    "cable_temp_warning_c": 55.0,    # 55°C uzeri uyaridir
    "cable_temp_critical_c": 68.0,   # 68°C uzeri kritik asiri isinmadir (yangin/erime korumasi)
    
    # Sebeke Voltaj Esikleri (Faz-Notr 230V Nominal - TS EN 50160 %10 Tolerans)
    "voltage_min_v": 207.0,          # 230V - %10 altinda düşük voltaj arizasi
    "voltage_max_v": 253.0,          # 230V + %10 ustunde aşırı voltaj arizasi
    
    # Mekanik ve Baglanti Guvenilirligi
    "max_consecutive_errors": 3,     # Arka arkaya 3 iptal/hata kilit mekanizma arizasini isaret eder
    "min_expected_power_kw_ratio": 0.50 # Talep edilenin %50'sinden az guc verilirse modül arizasi
}
