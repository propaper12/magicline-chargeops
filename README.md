# ⚡ ChargeOps AI
### Autonomous EV Charging Station Telemetry, Predictive Maintenance & Grid Load Intelligence

> **Magicline Enerji Sistemleri Sanayi ve Ticaret Ltd. Şti. (EPDK Lisanslı Şarj Ağı İşletmecisi / CPO) İçin Özel Olarak Geliştirilmiş Uçtan Uca Telemetri ve Kestirimci Bakım Platformu**

---

## 📌 Proje Vizyonu ve Sektörel Problem

Türkiye'de elektrikli araç (EV) şarj ağı işletmeciliğinde (CPO) en büyük maliyet ve itibar kaybı **istasyon kesintileri (downtime)** ve **şebeke aşırı yük cezalarıdır**:

1. **İstasyon Arızaları ve Termal Erime:** Saha şarj istasyonlarında (özellikle DC 120kW - 180kW hızlı şarj ünitelerinde) soket pinlerinin aşırı ısınması (>68°C), kablo yıpranması veya şebeke voltaj dalgalanması (207V altına düşüş) istasyonları devre dışı bırakır. Sürücü istasyona geldiğinde şarj edemez, ciro ve müşteri güveni kaybedilir.
2. **Reaktif Bakım Darboğazı:** Geleneksel sistemlerde arıza ancak kullanıcı çağrı merkezini aradığında veya istasyon tamamen sustuğunda fark edilir.
3. **Pik Şebeke Yükü:** İş çıkışı saatlerinde (18:00 - 20:00) aynı anda birden fazla aracın hızlı şarj olması trafo kapasitesini zorlar ve yüksek enerji maliyetlerine yol açar.

**ChargeOps AI**, OCPP 1.6J / 2.0.1 telemetri akışını (MeterValues) anlık olarak işleyerek arızaları **24-48 saat önceden tahmin eder (Predictive Maintenance)** ve dinamik yük dengeleme (Peak Shaving) ile enerji maliyetlerini optimize eder.

---

## 🏛️ Mimari ve Çözüm Şeması

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
  │          ChargeOps CPO Dashboard (FastAPI + Tailwind + Chart.js)       │
  │   • Canlı İstasyon Ağı ve Sağlık Skorları (% Uptime, Arıza Isı Haritası)│
  │   • Anlık Telemetri Grafikleri (kW Güç, Sıcaklık, Voltaj Dalgalanması) │
  │   • Otomatik Bakım Bildirimleri & Saha Ekibi Yönlendirme Kartları      │
  └────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Temel Yetkinlikler

### 1. Kestirimci Bakım Motoru (Predictive Maintenance)
- **Termal Aşırı Isınma Kalkanı:** Kablo ve soket sıcaklığı 55°C üzerine çıktığında uyarı, 68°C kritik eşiğini zorladığında acil duruş önleme bileti üretir.
- **Şebeke Voltaj Stabilitesi:** 230V nominal şebekenin ±%10 tolerans dışına (207V altı veya 253V üstü) saptığı lokasyonları tespit ederek güç modülü hasarlarını engeller.
- **Otomatik Saha Görevlendirmesi:** Arıza tipi, tahmini duruş saati (örn: 24 saat içinde) ve yapılması gereken somut aksiyonu içeren bakım kartları derler.

### 2. Şebeke Yük & Talep Tahminleme (Grid Load & Demand)
- **24 Saatlik Tüketim Eğrisi:** Seans bazlı enerji (kWh) ve güç (kW) eğrisini analiz ederek pik saatleri (18:00 - 20:00) saptar.
- **Dinamik Yük Dengeleme (DLB):** Pik saatlerde trafo cezalarını önlemek için güç sınırı algoritmaları önerir.
- **CPO Finansal Raporlama:** İstasyon bazlı ciro (TL), ortalama seans süresi ve enerji satış hacmini modeller.

### 3. Gerçek Zamanlı CPO Operasyon Kokpiti
- Modern, koyu modlu Tailwind CSS ve Chart.js tabanlı arayüz.
- İstasyon bazlı anlık telemetri paneli ve tek tıkla saha ekibine yönlendirme mekanizması.

---

## 📂 Proje Dizin Yapısı

```
magicline-chargeops/
├── database/
│   ├── __init__.py
│   ├── connection.py           # DuckDB in-memory bağlantı yöneticisi
│   └── seed_data.py            # OCPP telemetri ve seans veri ambarı üreticisi
├── engines/
│   ├── __init__.py
│   ├── predictive_engine.py    # Kestirimci bakım ve telemetri anomali motoru
│   └── forecasting_engine.py   # Şebeke yükü ve talep tahminleme motoru
├── web/
│   └── index.html              # Tailwind CSS & Chart.js tabanlı CPO operasyon paneli
├── tests/
│   └── test_chargeops.py       # 4/4 geçen birim ve entegrasyon test paketi
├── config.py                   # EPDK tarifeleri, sıcaklık ve voltaj eşikleri
├── main.py                     # FastAPI REST API servisi
├── run.py                      # Tek komutla başlatma entrypoint'i
├── requirements.txt            # Python bağımlılıkları
├── PROJECT_BLUEPRINT.md        # Mimari plan ve Magicline gereksinim dökümü
└── README.md                   # Proje dokümantasyonu
```

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Telemetri ve Seans Verilerini Üretin
```bash
python -m database.seed_data
```
*(6 şarj istasyonu, 12 soket, 1.200 seans ve 8.000 OCPP telemetri logu üretilir).*

### 3. Uygulamayı Başlatın
```bash
python run.py
```
*Arayüz `http://127.0.0.1:8002` adresinde canlı yayına başlar.*

### 4. Testleri Koşun
```bash
python -m unittest tests/test_chargeops.py
```

---

## 👨‍💻 Geliştirici

**Ömer Çakan**  
*Yönetim Bilişim Sistemleri (YBS / MIS) 2026 Mezunu*  
*Data & AI Engineer*  
- **LinkedIn:** [linkedin.com/in/ömer-çakan-819751261](https://www.linkedin.com/in/ömer-çakan-819751261)  
- **GitHub:** [github.com/propaper12](https://github.com/propaper12)  
- **Teknoloji Odağı:** EV Şarj Telemetrisi (OCPP), Kestirimci Bakım (Predictive Maintenance), DuckDB Columnar Analitik, Python & FastAPI.
