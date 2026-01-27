import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Konfigurasi Halaman ---
st.set_page_config(page_title="UAS Big Data Dashboard", layout="wide")

# --- 2. Load Data ---
@st.cache_data
def load_data():
    try:
        df_country = pd.read_csv("output_country_stats.csv")
        df_products = pd.read_csv("output_top_products.csv")
        df_trend = pd.read_csv("output_sales_trend.csv")
        return df_country, df_products, df_trend
    except FileNotFoundError:
        return None, None, None

df_country, df_products, df_trend = load_data()

# --- 3. Sidebar (Filter) ---
st.sidebar.header("🎛️ Panel Kontrol")
st.sidebar.write("Gunakan filter di bawah ini untuk melihat detail per negara.")

if df_country is not None:
    all_countries = df_country['Country'].unique().tolist()
    # Default ke United Kingdom agar tampilan awal langsung terisi data menarik
    selected_country = st.sidebar.selectbox("Pilih Negara Fokus:", ["All"] + all_countries)
else:
    selected_country = "All"

# --- 4. Main Layout ---
st.title("📊 Dashboard Analisis Big Data Retail")
st.markdown("### 1. Global Overview (Konteks Makro)")
st.write("Gambaran umum performa bisnis di seluruh dunia.")

if df_country is not None:
    # --- BAGIAN ATAS: GLOBAL STATIS (Tidak Terpengaruh Filter) ---
    col_global_1, col_global_2 = st.columns([2, 1])

    with col_global_1:
        # Line Chart Global Trend
        fig_trend = px.line(df_trend, x='YearMonth', y='MonthlyRevenue', 
                            title='Tren Pendapatan Global (Per Bulan)', markers=True)
        # Sedikit styling agar lebih clean
        fig_trend.update_layout(xaxis_title="Bulan", yaxis_title="Total Revenue (£)")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_global_2:
        # Bar Chart Top 10 Countries (Ranking)
        top_countries = df_country.head(10).sort_values(by="TotalRevenue", ascending=True) # Ascending agar bar terpanjang di atas di chart horizontal
        fig_country = px.bar(top_countries, x='TotalRevenue', y='Country', orientation='h',
                             title='Top 10 Negara (Kontribusi Pendapatan)', 
                             text_auto='.2s') # text_auto untuk menampilkan angka di bar
        fig_country.update_layout(xaxis_title="Total Revenue", yaxis_title="")
        st.plotly_chart(fig_country, use_container_width=True)

    st.markdown("---") # Garis pemisah visual

    # --- BAGIAN BAWAH: DINAMIS (Berubah sesuai Filter) ---
    
    # Tentukan Label Tampilan
    if selected_country == "All":
        display_name = "Global (Semua Negara)"
        # Logika: Jika All, hitung sum dari semua
        current_revenue = df_country['TotalRevenue'].sum()
        current_trx = df_country['TotalTransactions'].sum()
        # Chart produk ambil default (UK) atau Global top jika ada
        chart_data = df_products[df_products['Country'] == 'United Kingdom'] 
        sub_title = "Top Produk Global (Didominasi UK)"
    else:
        display_name = f"Negara: {selected_country}"
        # Filter data
        filtered_stats = df_country[df_country['Country'] == selected_country]
        if not filtered_stats.empty:
            current_revenue = filtered_stats['TotalRevenue'].values[0]
            current_trx = filtered_stats['TotalTransactions'].values[0]
        else:
            current_revenue = 0
            current_trx = 0
        
        chart_data = df_products[df_products['Country'] == selected_country]
        sub_title = f"Top 5 Produk Terlaris di {selected_country}"

    st.markdown(f"### 2. Deep Dive Analysis: {display_name}")
    
    # KPI Metrics
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="💰 Total Pendapatan", value=f"£ {current_revenue:,.2f}")
    with kpi2:
        st.metric(label="🧾 Total Transaksi", value=f"{current_trx:,.0f} Trx")
    with kpi3:
        # Contoh metrik tambahan dummy atau hitungan rata-rata
        avg_basket = current_revenue / current_trx if current_trx > 0 else 0
        st.metric(label="🛒 Rata-rata Nilai Keranjang", value=f"£ {avg_basket:,.2f}")

    # Chart Produk Dinamis
    st.subheader(f"🏆 {sub_title}")
    
    if not chart_data.empty:
        fig_prod = px.bar(chart_data, x='TotalQty', y='Description', 
                          color='TotalQty', color_continuous_scale='Viridis',
                          text_auto=True)
        fig_prod.update_layout(xaxis_title="Jumlah Terjual (Qty)", yaxis_title="Nama Produk", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.warning(f"Tidak ada data produk yang cukup signifikan untuk ditampilkan di {selected_country}.")

else:
    st.error("Data tidak ditemukan. Jalankan 'spark_etl.py' terlebih dahulu!")