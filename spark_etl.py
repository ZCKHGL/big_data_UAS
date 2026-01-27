import sys
import os

# --- BAGIAN INI SANGAT PENTING DI WINDOWS ---
import findspark
# Inisialisasi findspark. Ini akan mencari folder instalasi Spark secara otomatis
# atau menggunakan SPARK_HOME jika sudah diset.
findspark.init()
# --------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, to_date, desc, row_number, expr
from pyspark.sql.window import Window

def run_spark_etl():
    print("--- Memulai Spark ETL Job ---")
    
    # 1. Init Spark
    # Menambahkan konfigurasi memory agar tidak crash di local
    spark = SparkSession.builder \
        .appName("UAS_Retail_ETL") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    # 2. Baca dari HDFS
    # Pastikan path ini benar. Jika error "Path does not exist", 
    # coba ganti "hdfs://localhost:9000/..." atau "/" saja tergantung config Hadoop Anda
    hdfs_path = "/user/bigdata/uas_project/raw/online_retail_II.csv"
    
    print(f"Membaca data dari: {hdfs_path}")
    
    try:
        df = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(hdfs_path)
    except Exception as e:
        print(f"Error membaca HDFS: {e}")
        print("Pastikan Hadoop (Namenode/Datanode) sudah berjalan!")
        return

    # 3. Cleaning
    print("Sedang melakukan cleaning...")
    df_clean = df.dropna(subset=["Customer ID"]) \
                 .filter(~col("Invoice").like("C%")) \
                 .filter(col("Quantity") > 0)

    df_clean = df_clean.withColumn("TotalAmount", col("Quantity") * col("Price")) \
                       .withColumn("InvoiceDate", to_date(col("InvoiceDate"), "M/d/yyyy H:mm"))

    # 4. Complex Logic 1: Aggregation per Negara
    print("Menghitung statistik negara...")
    country_stats = df_clean.groupBy("Country") \
        .agg(sum("TotalAmount").alias("TotalRevenue"), count("Invoice").alias("TotalTransactions")) \
        .orderBy(desc("TotalRevenue"))

    # 5. Complex Logic 2: Top Product per Negara
    print("Mencari top produk...")
    windowSpec = Window.partitionBy("Country").orderBy(desc("TotalQty"))
    product_sales = df_clean.groupBy("Country", "Description") \
        .agg(sum("Quantity").alias("TotalQty"))
    
    top_products = product_sales.withColumn("Rank", row_number().over(windowSpec)) \
        .filter(col("Rank") <= 5)

    # 6. Complex Logic 3: Trend Bulanan
    print("Menghitung tren bulanan...")
    sales_trend = df_clean.withColumn("YearMonth", expr("substring(InvoiceDate, 1, 7)")) \
        .groupBy("YearMonth") \
        .agg(sum("TotalAmount").alias("MonthlyRevenue")) \
        .orderBy("YearMonth")

    # 7. SAVE OUTPUT KE LOKAL
    print("Menyimpan hasil olahan ke CSV lokal...")
    
    # Gunakan try-except untuk menangkap error saat save
    try:
        country_stats.toPandas().to_csv("output_country_stats.csv", index=False)
        top_products.toPandas().to_csv("output_top_products.csv", index=False)
        sales_trend.toPandas().to_csv("output_sales_trend.csv", index=False)
        print("--- ETL Selesai. Data siap untuk Streamlit! ---")
    except Exception as e:
        print(f"Gagal menyimpan CSV: {e}")
        
    spark.stop()

if __name__ == "__main__":
    run_spark_etl()