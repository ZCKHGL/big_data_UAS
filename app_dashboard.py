import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURATION & ASSETS ---
st.set_page_config(
    page_title="Retail Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# --- 2. MULTI-LANGUAGE DICTIONARY (KAMUS) ---
# Ini adalah otak dari fitur translasi. 
# Format: "key_unik": {"en": "Text English", "id": "Teks Indonesia"}
LANG = {
    "sidebar_title": {"en": "Control Panel", "id": "Panel Kontrol"},
    "sidebar_instr": {"en": "Use filters below to isolate country performance.", "id": "Gunakan filter untuk melihat detail negara."},
    "sel_country":   {"en": "Select Region/Country", "id": "Pilih Wilayah/Negara"},
    "opt_all":       {"en": "All Global Operations", "id": "Semua Operasi Global"},
    "data_source":   {"en": "Data Source: Retail Big Data ETL Pipeline v1.2", "id": "Sumber Data: Pipa ETL Big Data Ritel v1.2"},
    
    "main_title":    {"en": "Retail Intelligence Dashboard", "id": "Dashboard Intelijen Ritel"},
    "main_subtitle": {"en": "Real-time analysis of transaction flows and product performance.", "id": "Analisis real-time arus transaksi dan performa produk."},
    "status":        {"en": "System Online", "id": "Sistem Online"},
    
    "perf_title":    {"en": "Performance:", "id": "Performa:"},
    "kpi_rev":       {"en": "Total Revenue", "id": "Total Pendapatan"},
    "kpi_rev_desc":  {"en": "Total Gross Revenue for selected period", "id": "Total pendapatan kotor periode terpilih"},
    "kpi_trx":       {"en": "Total Transactions", "id": "Total Transaksi"},
    "kpi_trx_desc":  {"en": "Count of unique invoices processed", "id": "Jumlah faktur unik yang diproses"},
    "kpi_avg":       {"en": "Avg. Basket Value", "id": "Rata-rata Nilai Keranjang"},
    "kpi_avg_desc":  {"en": "Average revenue per transaction", "id": "Pendapatan rata-rata per transaksi"},
    
    "chart_trend":   {"en": "Revenue Trend Analysis", "id": "Analisis Tren Pendapatan"},
    "chart_rank":    {"en": "Top Markets by Revenue", "id": "Pasar Teratas berdasarkan Pendapatan"},
    
    "prod_section":  {"en": "Top Products", "id": "Produk Unggulan"},
    "prod_global":   {"en": "Global Top Products (Market Driver: UK)", "id": "Produk Top Global (Didominasi UK)"},
    "prod_local":    {"en": "Top Performing Products:", "id": "Produk Terlaris:"},
    "warn_nodata":   {"en": "Insufficient product data for", "id": "Data produk tidak cukup untuk"},
    "warn_disc":     {"en": "Data Source Disconnected.", "id": "Sumber Data Terputus."},
    "units_sold":    {"en": "Units Sold", "id": "Unit Terjual"}
}

# --- 3. CUSTOM CSS INJECTION ---
st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0" />
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0E1117; }
    
    /* Custom Card Styling */
    .metric-card {
        background-color: #1E212B;
        border: 1px solid #2B303B;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #4E8CFF;
    }
    
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    
    .metric-value {
        font-size: 28px; font-weight: 700; color: #4E8CFF; margin-top: 5px;
    }
    .metric-label {
        font-size: 14px; color: #A0A0A0; display: flex; align-items: center; gap: 8px;
    }
    .material-symbols-rounded { font-size: 20px; vertical-align: middle; }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] { background-color: #12151C; border-right: 1px solid #2B303B; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---

# Function untuk mengambil text berdasarkan bahasa
def get_txt(key):
    lang_code = st.session_state.get('language', 'en') # Default English
    return LANG[key][lang_code]

# HTML Card
def html_card(title, value, icon_name, tooltip=""):
    st.markdown(f"""
    <div class="metric-card" title="{tooltip}">
        <div class="metric-label">
            <span class="material-symbols-rounded">{icon_name}</span>
            {title}
        </div>
        <div class="metric-value">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Update bagian load_data ---
@st.cache_data
def load_data():
    required_files = [
        "output_country_stats.csv",
        "output_top_products.csv",
        "output_sales_trend.csv"
    ]
    
    # Cek apakah semua file ada
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        st.error(f"❌ File data hilang: {', '.join(missing_files)}")
        st.warning("Pastikan Anda sudah menjalankan 'spark_etl.py' di lokal DAN meng-upload file CSV hasilnya ke GitHub!")
        return None, None, None

    try:
        df_country = pd.read_csv("output_country_stats.csv")
        df_products = pd.read_csv("output_top_products.csv")
        df_trend = pd.read_csv("output_sales_trend.csv")
        return df_country, df_products, df_trend
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        return None, None, None

# --- 5. SIDEBAR ---
with st.sidebar:
    # LANGUAGE SWITCHER
    st.markdown('### 🌐 Language / Bahasa')
    
    # Radio button horizontal untuk memilih bahasa
    lang_choice = st.radio(
        "Pilih Bahasa:", 
        ('English', 'Bahasa Indonesia'), 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Simpan pilihan ke session state
    if lang_choice == 'English':
        st.session_state['language'] = 'en'
    else:
        st.session_state['language'] = 'id'

    st.markdown("---")

    # Menggunakan get_txt() untuk label dinamis
    st.markdown(f'### <span class="material-symbols-rounded">tune</span> {get_txt("sidebar_title")}', unsafe_allow_html=True)
    st.write(get_txt("sidebar_instr"))
    
    if df_country is not None:
        all_countries = sorted(df_country['Country'].unique().tolist())
        # Kita translate opsi "All Global Operations"
        display_options = [get_txt("opt_all")] + all_countries
        
        selected_option = st.selectbox(
            get_txt("sel_country"), 
            display_options,
            index=0
        )
        
        # Mapping balik dari Display Name ke Real Data Value
        if selected_option == get_txt("opt_all"):
            selected_country = "All"
        else:
            selected_country = selected_option
            
    else:
        selected_country = "All"
        
    st.caption(get_txt("data_source"))

# --- 6. MAIN CONTENT ---

# Header Section
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title(get_txt("main_title"))
    st.markdown(get_txt("main_subtitle"))
with col_header_2:
    st.markdown(f"""
        <div style="text-align: right; padding-top: 20px; color: #00C853;">
            <span class="material-symbols-rounded">wifi</span> {get_txt("status")}
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

if df_country is not None:
    
    # =================================================================
    # SECTION 1: MACRO OVERVIEW (STATIC - SELALU GLOBAL)
    # =================================================================
    st.markdown(f"### 🌏 Global Overview")
    st.caption("General market performance across all regions (Static View)")

    col_viz_1, col_viz_2 = st.columns([2, 1])

    with col_viz_1:
        # Chart 1: Global Trend
        fig_trend = px.area(df_trend, x='YearMonth', y='MonthlyRevenue', 
                            title=f"<b>{get_txt('chart_trend')}</b>", markers=True)
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0', family="Inter"),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#2B303B'),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350 # Sedikit dipendekkan agar KPI dibawahnya terlihat
        )
        fig_trend.update_traces(line_color='#4E8CFF', fillcolor='rgba(78, 140, 255, 0.2)')
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_viz_2:
        # Chart 2: Top Countries Ranking
        top_countries = df_country.head(10).sort_values(by="TotalRevenue", ascending=True)
        fig_country = px.bar(top_countries, x='TotalRevenue', y='Country', orientation='h',
                             title=f"<b>{get_txt('chart_rank')}</b>", text_auto='.2s')
        fig_country.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0', family="Inter"),
            xaxis=dict(showgrid=True, gridcolor='#2B303B'), yaxis=dict(title=""),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350 # Samakan tinggi dengan chart sebelah
        )
        fig_country.update_traces(marker_color='#00E676', textfont_color='white')
        st.plotly_chart(fig_country, use_container_width=True)

    # Garis pemisah yang tegas
    st.markdown("---") 

    # =================================================================
    # SECTION 2: REGIONAL DEEP DIVE (DYNAMIC - BERUBAH SESUAI FILTER)
    # =================================================================
    
    # 1. Hitung Logika Filter dulu
    if selected_country == "All":
        display_name = "Global"
        current_revenue = df_country['TotalRevenue'].sum()
        current_trx = df_country['TotalTransactions'].sum()
        chart_data = df_products[df_products['Country'] == 'United Kingdom']
        sub_title = get_txt("prod_global")
    else:
        display_name = selected_country
        filtered_stats = df_country[df_country['Country'] == selected_country]
        if not filtered_stats.empty:
            current_revenue = filtered_stats['TotalRevenue'].values[0]
            current_trx = filtered_stats['TotalTransactions'].values[0]
        else:
            current_revenue = 0
            current_trx = 0
        chart_data = df_products[df_products['Country'] == selected_country]
        sub_title = f"{get_txt('prod_local')} {selected_country}"

    avg_basket = current_revenue / current_trx if current_trx > 0 else 0

    # 2. Tampilkan Judul Bagian Dinamis
    st.markdown(f"### <span class='material-symbols-rounded'>filter_alt</span> Deep Dive Analysis: {display_name}", unsafe_allow_html=True)
    
    # 3. Tampilkan KPI Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        html_card(get_txt("kpi_rev"), f"£ {current_revenue:,.2f}", "payments", get_txt("kpi_rev_desc"))
    with kpi2:
        html_card(get_txt("kpi_trx"), f"{current_trx:,.0f}", "receipt_long", get_txt("kpi_trx_desc"))
    with kpi3:
        html_card(get_txt("kpi_avg"), f"£ {avg_basket:,.2f}", "shopping_basket", get_txt("kpi_avg_desc"))

    st.markdown("###") # Spacer

    # 4. Tampilkan Product Chart
    st.markdown(f"#### <span class='material-symbols-rounded'>inventory_2</span> {sub_title}", unsafe_allow_html=True)

    if not chart_data.empty:
        fig_prod = px.bar(chart_data, x='TotalQty', y='Description', 
                          color='TotalQty', color_continuous_scale='Bluyl',
                          text_auto=True, orientation='h')
        fig_prod.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0', family="Inter"),
            xaxis=dict(showgrid=True, gridcolor='#2B303B', title=get_txt("units_sold")),
            yaxis=dict(title="", categoryorder='total ascending'),
            margin=dict(l=0, r=0, t=0, b=0), height=400
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.info(f"{get_txt('warn_nodata')} {selected_country}.")

else:
    st.warning(f"⚠ {get_txt('warn_disc')}")