# ⚡ ChargeOps AI — Proje Mimari Planı & Teknik Blueprint
### Elektrikli Araç (EV) Şarj İstasyonları İçin Otonom Telemetri, Kestirimci Bakım & Yük Analitiği Platformu

> **Hedef Şirket:** Magicline Enerji Sistemleri Sanayi ve Ticaret Ltd. Şti.  
> **Sektör:** Elektrikli Araç Şarj Ağı İşletmeciliği (EPDK Lisanslı CPO - Charge Point Operator) & Yenilenebilir Enerji  
> **Geliştirici:** Ömer Çakan (Data & AI Engineer / Yönetim Bilişim Sistemleri '26)  
> **Konum:** `C:\Users\omerc\Desktop\magicline-chargeops`

---

## 1. 🎯 Projenin Çıkış Noktası ve Magicline Enerji İhtiyacı

Türkiye'de hızla büyüyen elektrikli araç (EV) pazarında şarj ağı işletmecilerinin (CPO) karşılaştığı **en büyük 3 operasyonel ve finansal kriz:**

1. **İstasyon Kesintileri ve Arızalar (Downtime Maliyeti):**
   - Saha istasyonlarında soket kilit hataları (Connector Lock Failure), aşırı kablo ısınması (Overheating), toprak kaçağı veya voltaj dalgalanması yaşandığında istasyon devre dışı kalır.
   - Sürücü istasyona gelip şarj edemediğinde müşteri kaybedilir, EPDK hizmet kalitesi standartları riske girer ve ciro kaybı yaşanır.
   - *Mevcut Durum:* Arıza ancak sürücü çağrı merkezini aradığında fark edilir (Reaktif).
   - *ChargeOps AI Çözümü:* Telemetri loglarından (sıcaklık, voltaj sapması) arızayı 24-48 saat önceden tahmin edip bakım bileti açar (Kestirimci / Predictive).

2. **Şebeke Gücü ve Dinamik Yük Yönetimi (Dynamic Load Balancing - DLB):**
   - Özellikle DC hızlı şarj (60kW - 180kW) istasyonlarında aynı anda birden fazla araç şarj olduğunda trafo kapasitesi zorlanır, elektrik pik tarifesi tavan yapar.
   - *ChargeOps AI Çözümü:* İstasyon bazlı anlık güç tüketimini izler, pik saatleri tahmin eder ve yükü optimize eden zeki dağıtım modelleri önerir.

3. **Veri Körlüğü & Yatırım Fizibilitesi (CPO Analytics):**
   - Hangi istasyon günün hangi saatinde ne kadar doluluk oranına ulaşıyor? Hangi lokasyona yeni bir DC ünitesi kurulmalı?
   - *ChargeOps AI Çözümü:* Geçmiş şarj seanslarından (kWh, süre, araç batarya doluluk oranı - SoC) talep ve gelir tahminlemesi yaparak yatırım kararlarını yapay zeka ile destekler.

---

## 2. 🏛️ Sistem Mimarisi & Teknoloji Yığını

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   Magicline Sahadaki Şarj İstasyonları                 │
  │              (AC 22kW / DC 60kW - 180kW Çift Soketli Üniteler)         │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │  OCPP 1.6J / 2.0.1 Telemetri Akışı
                                      │  (Voltaj, Akım, Sıcaklık, Hata Kodları)
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                 ChargeOps AI: Çekirdek Telemetri Katmanı               │
  │     (DuckDB Columnar Veri Motoru + Sentetik OCPP Simülatörü)          │
  └───────────────────┬───────────────────────────────┬────────────────────┘
                      │                               │
                      ▼                               ▼
       ┌──────────────────────────────┐ ┌──────────────────────────────┐
       │   Kestirimci Bakım Motoru    │ │    Talep & Gelir Tahmin      │
       │ (Predictive Maintenance AI)  │ │      (Demand Forecasting)    │
       │  • Aşırı Isınma Analizi      │ │  • Saatlik Doluluk Tahmini   │
       │  • Voltaj Dengesizliği       │ │  • EPDK Gelir Raporlaması    │
       │  • Soket Kilit Aşınması      │ │  • Dinamik Yük Dağıtımı      │
       └──────────────┬───────────────┘ └──────────────┬───────────────┘
                      │                                │
                      └───────────────┬────────────────┘
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                    FastAPI Yüksek Hızlı REST API                       │
  │              (İstasyon Durumları, Anomali Uyarıları, Seanslar)         │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │          ChargeOps CPO Dashboard (Tailwind CSS + Chart.js)             │
  │   • Canlı İstasyon Ağı ve Sağlık Skorları (% Uptime, Arıza Isı Haritası)│
  │   • Anlık Telemetri Grafikleri (kW Güç, Sıcaklık, Voltaj Dalgalanması) │
  │   • Otomatik Bakım Bildirimleri & Saha Ekibi Yönlendirme Kartları      │
  └────────────────────────────────────────────────────────────────────────┘
```

### Teknoloji Yığını:
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Veri Motoru:** DuckDB (İn-Memory Columnar Lakehouse — OCPP telemetrisi ve seans logları için ultra hızlı analitik)
- **Veri Bilimi / ML:** Scikit-Learn / NumPy (Anomali tespiti ve trend varyansı)
- **Protokol Standardı:** OCPP 1.6J / 2.0.1 uyumlu veri modelleri (MeterValues, StatusNotification, StopTransaction)
- **Frontend:** Tailwind CSS, FontAwesome, Chart.js (Modern koyu modlu CPO Operasyon Kokpiti)

---

## 3. 📊 Veri Modeli & Şema Tasarımı

### 1. `stations` (İstasyon Varlıkları)
- `station_id` (VARCHAR PK - örn: `ML-IST-001`)
- `station_name` (VARCHAR - örn: `Tekstilkent Plaza DC Hızlı Şarj`)
- `city` / `district` (VARCHAR - Lokasyon)
- `station_type` (VARCHAR - `DC_FAST` [120kW], `AC_NORMAL` [22kW])
- `total_connectors` (INT - 2 soket)
- `max_power_kw` (DOUBLE - 120.0)
- `installation_date` (TIMESTAMP)
- `firmware_version` (VARCHAR - `v2.4.1`)
- `current_status` (VARCHAR - `Available`, `Charging`, `Faulted`, `Offline`)

### 2. `connectors` (Soket Durumları)
- `connector_id` (VARCHAR PK - örn: `ML-IST-001-C1`)
- `station_id` (VARCHAR FK)
- `connector_type` (VARCHAR - `CCS2`, `CHAdeMO`, `Type2`)
- `max_current_amp` (DOUBLE)
- `status` (VARCHAR - `Available`, `Occupied`, `Preparing`, `SuspendedEV`)

### 3. `telemetry_logs` (OCPP MeterValues Akışı — 10.000+ Kayıt)
- `log_id` (VARCHAR PK)
- `station_id` (VARCHAR FK)
- `connector_id` (VARCHAR FK)
- `voltage_v` (DOUBLE - Şebeke voltajı: Normalde 230V / 400V)
- `current_a` (DOUBLE - Çekilen akım)
- `active_power_kw` (DOUBLE - Anlık güç)
- `cable_temperature_c` (DOUBLE - Kablo/soket sıcaklığı: Kritik eşik > 65°C)
- `soc_pct` (INT - Araç batarya doluluk oranı %0-100)
- `error_code` (VARCHAR - `NoError`, `OverTemperature`, `HighVoltage`, `ConnectorLockFailure`)
- `timestamp` (TIMESTAMP)

### 4. `charging_sessions` (Tamamlanan Şarj Seansları)
- `session_id` (VARCHAR PK - örn: `SES-9821`)
- `station_id` (VARCHAR FK)
- `connector_id` (VARCHAR FK)
- `user_rfid_or_app_id` (VARCHAR)
- `energy_delivered_kwh` (DOUBLE - Verilen enerji)
- `total_price_tl` (DOUBLE - Ücret)
- `start_time` / `end_time` (TIMESTAMP)
- `duration_minutes` (INT)
- `stop_reason` (VARCHAR - `EVDisconnected`, `LocalStop`, `EmergencyStop`, `Fault`)

### 5. `maintenance_tickets` (Kestirimci Bakım & Anomali Kayıtları)
- `ticket_id` (VARCHAR PK - örn: `TCK-001`)
- `station_id` (VARCHAR FK)
- `anomaly_type` (VARCHAR - `OVERHEATING_RISK`, `VOLTAGE_FLUCTUATION`, `LOCK_WEAR`)
- `severity` (VARCHAR - `CRITICAL`, `WARNING`, `INFO`)
- `predicted_failure_hours` (INT - Tahmini arıza süresi: örn 36 saat)
- `recommended_action` (TEXT - "Saha ekibine CCS2 soket kontak temizliği ve sıcaklık sensörü kontrolü atandı.")
- `created_at` (TIMESTAMP)
- `is_resolved` (BOOLEAN)

---

## 4. 🧠 Yapay Zeka & Analitik Motor Modülleri

### Modül 1: Kestirimci Bakım & Telemetri Anomali Motoru (`predictive_engine.py`)
- **Aşırı Isınma (Thermal Degradation):** Son 5 şarj seansında kablo sıcaklığının ortalama 58°C üzerine çıktığı ve her seansta +2°C artış trendi sergilediği istasyonları algılar.
- **Voltaj Dengesizliği (Grid Power Anomaly):** Şebeke voltajı 210V altına veya 250V üstüne saptığında şarj ünitesinin güç modülünün zarar görmesini engellemek için uyarı üretir.
- **Soket Kilit Hatası (Connector Wear):** Arka arkaya iptal edilen (`EmergencyStop` veya `LockError`) seansları analiz edip mekanik kilit aşınmasını tespit eder.

### Modül 2: İstasyon Yük & Gelir Tahminleme Motoru (`forecasting_engine.py`)
- Saatlik ve günlük bazda şarj talebini modeller.
- Hafta içi iş çıkış saatleri (17:30 - 20:00) ile hafta sonu AVM/otoyol kullanım piklerini analiz eder.
- Dinamik enerji fiyatı (EPDK zaman dilimli tarifeler) ve trafo kapasitesine göre optimal şarj stratejisi sunar.

### Modül 3: CPO Yönetici Raporlayıcısı (`fleet_synthesizer.py`)
- Tüm şarj ağının genel sağlık skorunu (% Uptime, Ortalama Şarj Gücü, Aktif Arıza Sayısı) C-Level yönetici özeti halinde sentezler.

---

## 5. 💻 CPO Operasyon Paneli (Web UI Özellikleri)

1. **Üst KPI Paneli:**
   - Toplam Kurulu Güç (kW) & İstasyon Sayısı
   - Ağ Çalışma Süresi (Uptime %98.4)
   - Günlük Verilen Toplam Enerji (kWh) & Toplam Gelir (TL)
   - Aktif Kestirimci Bakım Bildirimleri (Kritik / Uyarı)

2. **İstasyon Ağı & Canlı Telemetri İzleme:**
   - İstasyon kartları (Kadıköy DC, Maslak Hızlı Şarj, Tekstilkent Merkez, Ataşehir AVM).
   - Anlık soket durumu (`Charging`, `Available`, `Faulted`).
   - Canlı telemetri göstergeleri (Anlık kW güç, kablo sıcaklığı °C, voltaj V).

3. **Kestirimci Bakım Radarı (Predictive Maintenance Hub):**
   - Arıza çıkmadan önce yakalanan anomali kartları.
   - Örnek: *"ML-IST-002 Soket B: Son 48 saatte sıcaklık 64°C seviyesine yaklaştı. 24 saat içinde aşırı ısınma kaynaklı duruş bekleniyor."*
   - Tek tıkla "Saha Ekibi Bildirimi Aç" butonu.

4. **Yük & Talep Analitiği (Interactive Chart.js):**
   - 24 saatlik enerji tüketim eğrisi (kW vs Saat).
   - En yoğun istasyonlar sıralaması ve lokasyon bazlı doluluk oranları.

---

## 6. 📅 Proje Uygulama Yol Haritası (Fazlar)

- **Faz 1: Dizin & Altyapı:**
  `C:\Users\omerc\Desktop\magicline-chargeops` dizinini oluşturma, `requirements.txt`, `config.py` ve DuckDB bağlantı altyapısı.
- **Faz 2: Sentetik OCPP Telemetri & Seans Veri Üreticisi (`seed_data.py`):**
  4 farklı Magicline istasyonu (DC ve AC), 8 soket, 1.200 seans ve 10.000 satırlık telemetri verisi (özellikle 1 istasyonda aşırı ısınma, 1 istasyonda voltaj dengesizliği anomalisi enjekte edilir).
- **Faz 3: Kestirimci Bakım & Anomali Motoru (`predictive_engine.py`):**
  Aşırı ısınma, kilit aşınması ve şebeke voltaj anomali tespiti + otomatik bilet üretimi.
- **Faz 4: Talep & Şebeke Yük Motoru (`forecasting_engine.py`):**
  Pik saatler, doluluk yüzdeleri ve gelir optimizasyon modeli.
- **Faz 5: FastAPI Backend (`main.py`) & Canlı CPO Paneli (`web/index.html`):**
  Tüm REST endpoint'leri ve koyu modlu, grafikli operasyon kokpiti.
- **Faz 6: Testler, GitHub Repo Push & Magicline Outreach Metni:**
  Birim testler, `propaper12/magicline-chargeops` reposu ve şirket yöneticilerine özel iş başvuru metinleri.
