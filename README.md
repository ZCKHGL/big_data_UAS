# 📊 Big Data Retail Analytics - End-to-End Data Pipeline

> **Proyek UAS Big Data**: Analisis transaksi retail menggunakan arsitektur terdistribusi dengan HDFS, Apache Spark, dan Streamlit Dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Spark](https://img.shields.io/badge/Apache%20Spark-4.1.1-orange?logo=apachespark)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53-red?logo=streamlit)
![Hadoop](https://img.shields.io/badge/Hadoop-HDFS-yellow?logo=apachehadoop)

---

## 📋 Daftar Isi

- [Overview](#-overview)
- [Arsitektur Pipeline](#-arsitektur-pipeline)
- [Tech Stack](#-tech-stack)
- [Struktur Project](#-struktur-project)
- [Instalasi & Setup](#-instalasi--setup)
- [Cara Menjalankan](#-cara-menjalankan)
- [Analisis Teknis](#-analisis-teknis)
- [Business Insights](#-business-insights)
- [Rekomendasi Bisnis](#-rekomendasi-bisnis)

---

## 🎯 Overview

Project ini membangun sebuah **End-to-End Data Pipeline** yang mensimulasikan lingkungan industri nyata. Data tidak diproses di satu tempat, melainkan menggunakan arsitektur **Terdistribusi (Distributed)** dan **Terpisah (Decoupled)**.

### Dataset
- **Nama**: Online Retail II Dataset
- **Sumber**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II)
- **Deskripsi**: Data transaksi retail online dari UK yang mencakup periode 01/12/2009 - 09/12/2011
- **Ukuran**: ~90 MB (1+ juta records)

---

## 🏗 Arsitektur Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        END-TO-END DATA PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │   INGESTION     │     │   PROCESSING    │     │    SERVING      │       │
│  │     LAYER       │────▶│     LAYER       │────▶│     LAYER       │       │
│  │                 │     │                 │     │                 │       │
│  │  ┌───────────┐  │     │  ┌───────────┐  │     │  ┌───────────┐  │       │
│  │  │   HDFS    │  │     │  │   Spark   │  │     │  │ Streamlit │  │       │
│  │  │           │  │     │  │  (ETL)    │  │     │  │ Dashboard │  │       │
│  │  │  Raw CSV  │  │     │  │           │  │     │  │           │  │       │
│  │  └───────────┘  │     │  └───────────┘  │     │  └───────────┘  │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
│  Fault-tolerant         In-memory                 Interactive               │
│  Scalable Storage       Processing                Visualization             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Layer Details

| Layer | Teknologi | Fungsi | Filosofi |
|-------|-----------|--------|----------|
| **Ingestion** | HDFS | Menyimpan raw dataset `online_retail_II.csv` | *Fault-tolerant* & *Scalable* storage |
| **Processing** | Apache Spark (PySpark) | ETL: Extract, Transform, Load | *In-memory processing* untuk volume besar |
| **Serving** | Streamlit + Plotly | Dashboard Interaktif | Menyajikan *insight* kepada end-user |

---

## 🛠 Tech Stack

| Kategori | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| **Storage** | Hadoop HDFS | 3.x | Distributed File System |
| **Processing** | Apache Spark | 4.1.1 | In-memory data processing |
| **Language** | Python | 3.9+ | Main programming language |
| **Visualization** | Streamlit | 1.53 | Web dashboard framework |
| **Charting** | Plotly | 6.5 | Interactive charts |
| **Data Analysis** | Pandas | 2.3 | Data manipulation |
| **Bridge** | findspark | 2.0 | Spark-Python bridge |

---

## 📁 Struktur Project

```
online_retail_UK/
├── 📄 spark_etl.py           # Script ETL menggunakan PySpark
├── 📄 app_dashboard.py       # Dashboard Streamlit
├── 📄 requirements.txt       # Python dependencies
├── 📄 .gitignore            # Git ignore rules
├── 📄 README.md             # Dokumentasi project (file ini)
│
├── 📊 [DATA FILES - Diabaikan Git]
│   ├── online_retail_II.csv       # Raw dataset (~90MB)
│   ├── output_country_stats.csv   # Hasil agregasi per negara
│   ├── output_sales_trend.csv     # Hasil tren penjualan bulanan
│   └── output_top_products.csv    # Hasil top produk per negara
│
└── 📁 venv/                  # Virtual environment (diabaikan Git)
```

---

## ⚙ Instalasi & Setup

### Prerequisites
- Python 3.9+
- Java JDK 8 atau 11 (untuk Spark)
- Apache Hadoop (HDFS)
- Apache Spark

### 1. Clone Repository
```bash
git clone <repository-url>
cd online_retail_UK
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Hadoop HDFS
```bash
# Start Hadoop services
start-dfs.sh  # Linux/Mac
# atau jalankan melalui Hadoop bin di Windows

# Buat direktori di HDFS
hdfs dfs -mkdir -p /user/bigdata/uas_project/raw

# Upload dataset ke HDFS
hdfs dfs -put online_retail_II.csv /user/bigdata/uas_project/raw/
```

### 5. Verifikasi Upload HDFS
```bash
hdfs dfs -ls /user/bigdata/uas_project/raw/
# Output: -rw-r--r--   online_retail_II.csv
```

---

## 🚀 Cara Menjalankan

### Step 1: Jalankan ETL Spark
```bash
python spark_etl.py
```
Output yang diharapkan:
```
--- Memulai Spark ETL Job ---
Membaca data dari: /user/bigdata/uas_project/raw/online_retail_II.csv
Sedang melakukan cleaning...
Menghitung statistik negara...
Mencari top produk...
Menghitung tren bulanan...
Menyimpan hasil olahan ke CSV lokal...
--- ETL Selesai. Data siap untuk Streamlit! ---
```

### Step 2: Jalankan Dashboard Streamlit
```bash
streamlit run app_dashboard.py
```
Dashboard akan terbuka di browser: `http://localhost:8501`

---

## 🔬 Analisis Teknis

### Data Cleaning (spark_etl.py)

| Operasi | Deskripsi | Kode |
|---------|-----------|------|
| **Drop Null Customer ID** | Menghapus transaksi tanpa ID Customer | `dropna(subset=["Customer ID"])` |
| **Filter Invoice Retur** | Menghapus invoice yang diawali 'C' (Cancelled/Return) | `filter(~col("Invoice").like("C%"))` |
| **Filter Quantity** | Hanya menyimpan quantity positif | `filter(col("Quantity") > 0)` |

### Feature Engineering

| Feature | Formula | Keterangan |
|---------|---------|------------|
| `TotalAmount` | `Quantity × Price` | Revenue per line item |
| `InvoiceDate` | `to_date(InvoiceDate)` | Konversi ke format date |
| `YearMonth` | `substring(InvoiceDate, 1, 7)` | Ekstraksi YYYY-MM untuk agregasi |

### Complex Logic (3 Operasi Lanjutan)

#### 1. Revenue Aggregation per Negara
```python
country_stats = df_clean.groupBy("Country") \
    .agg(sum("TotalAmount").alias("TotalRevenue"), 
         count("Invoice").alias("TotalTransactions")) \
    .orderBy(desc("TotalRevenue"))
```

#### 2. Window Function - Top Product Ranking
```python
windowSpec = Window.partitionBy("Country").orderBy(desc("TotalQty"))
top_products = product_sales \
    .withColumn("Rank", row_number().over(windowSpec)) \
    .filter(col("Rank") <= 5)
```

#### 3. Time-Series Aggregation
```python
sales_trend = df_clean \
    .withColumn("YearMonth", expr("substring(InvoiceDate, 1, 7)")) \
    .groupBy("YearMonth") \
    .agg(sum("TotalAmount").alias("MonthlyRevenue")) \
    .orderBy("YearMonth")
```

### Compliance Matrix

| Komponen | Syarat UAS | Implementasi | Status |
|----------|------------|--------------|--------|
| **Storage** | HDFS & Dokumentasi Loading | Data disimpan di HDFS (`hdfs dfs -put`) | ✅ Valid |
| **Processing** | Data Cleaning & Transformation | Drop null, filter retur, create TotalAmount | ✅ Valid |
| **Advanced Logic** | Min. 3 Manipulasi Kompleks | Revenue calc, Windowing rank, Time aggregation | ✅ Valid |
| **Visualisasi** | Library Python & 2+ Pertanyaan | Streamlit + Plotly (3 visualisasi) | ✅ Valid |

---

## 📈 Business Insights

### Pertanyaan 1: Bagaimana performa kesehatan finansial perusahaan?

> **Visualisasi**: Line Chart - Tren Pendapatan Bulanan

**Temuan:**
- Pendapatan bersifat **fluktuatif dengan pola musiman**
- Lonjakan signifikan di **Kuartal 4** (Oktober-Desember)
- Bisnis sangat bergantung pada **Holiday Season** (Natal & Tahun Baru)

### Pertanyaan 2: Siapa pasar terbesar dan potensial?

> **Visualisasi**: Horizontal Bar Chart - Top 10 Negara

**Temuan:**
- **United Kingdom** mendominasi mayoritas revenue
- **EIRE (Irlandia)**, **Jerman**, dan **Prancis** sebagai Top 3 di luar UK
- Terdapat permintaan lintas negara yang stabil di **Eropa Barat**

### Pertanyaan 3: Apa yang sebenarnya pelanggan beli?

> **Visualisasi**: Bar Chart - Top Products

**Temuan:**
- Produk terlaris adalah **"Novelty Gift"** dan **Dekorasi**
- Contoh: *"White Hanging Heart"*, *"Jumbo Bag"*
- Kuantitas tinggi per transaksi → banyak pembeli adalah **Reseller/Grosir**

---

## 💡 Rekomendasi Bisnis

### 1. Strategi Logistik Musiman 📦

| Fakta | Rekomendasi |
|-------|-------------|
| Lonjakan tajam di akhir tahun | **Stockpiling** mulai bulan **September** |
| Peak season: November-Desember | Jika stok kosong = **Opportunity Loss** terbesar |

### 2. Ekspansi Internasional 🌍

| Fakta | Rekomendasi |
|-------|-------------|
| Ketergantungan berlebihan pada UK | Ekspansi agresif ke **Jerman & Prancis** |
| Minat organik tinggi di Eropa | Buat **gudang distribusi lokal** di Jerman |

### 3. Segmentasi Pelanggan B2B 🤝

| Fakta | Rekomendasi |
|-------|-------------|
| Banyak transaksi dengan Quantity tinggi | Buat program loyalitas **"Wholesaler"** |
| Grosir = tulang punggung cash flow | Berikan **diskon volume** (>50 unit/item) |

---

## 📝 Kesimpulan

> *"Data mentah transaksi retail yang berantakan disimpan dengan aman di **HDFS**, diolah dengan **Spark** untuk membersihkan retur dan menghitung ranking penjualan, lalu disajikan lewat **Streamlit** — mengungkap bahwa kunci pertumbuhan bisnis ada di **Ekspansi Pasar Eropa** dan **Persiapan Stok Akhir Tahun**."*

---

## 📄 License

Project ini dibuat untuk keperluan **UAS Mata Kuliah Big Data**.

---

## 👤 Author

**Ananta Deva**  
NIM: 23201254
Program Studi: Teknik Informatika
Universitas: Institut Teknologi & Bisnis Asia Malang  

**Zacky Haigel Putra Sandy Asmara** 
NIM: 23201248 
Program Studi: Teknik Informatika
Universitas: Institut Teknologi & Bisnis Asia Malang  

---

<p align="center">
  <i>Built using HDFS, Spark, and Streamlit</i>
</p>
