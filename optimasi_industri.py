import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import base64

st.set_page_config(page_title="Optimasi PT Sinar Terang Mandiri", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #fffdf7;
    }
    h1 {
        color: #d2691e;
        text-align: center;
        font-size: 40px;
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #ffb347;
        color: white;
        font-weight: bold;
    }
    .stDownloadButton > button {
        background-color: #20c997;
        color: white;
        font-weight: bold;
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 300px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Tambahkan logo
st.markdown("<img src='https://mihzzrbqlgf1.cdn.shift8web.ca/wp-content/uploads/2021/01/Sinar-Terang-Logo.jpg' class='logo'>", unsafe_allow_html=True)

st.markdown("<h1>OPTIMASI PRODUKSI - PT SINAR TERANG MANDIRI</h1>", unsafe_allow_html=True)

st.markdown("""
<p style='font-size: 18px;'>
Aplikasi ini membantu PT. Sinar Terang Mandiri menentukan jumlah produksi optimal untuk dua produk:<br>
- Produk A: Blender<br>
- Produk B: Pemanggang Roti<br><br>
Tujuannya adalah untuk memaksimalkan keuntungan, dengan batasan waktu mesin yang tersedia per minggu.
</p>
""", unsafe_allow_html=True)

# INPUT
st.header("📥 Input Data Produksi")

col1, col2 = st.columns(2)
with col1:
    profit_X = st.number_input("Keuntungan Per unit Blender (Rp)", value=7000)
    labor_X = st.number_input("Jam kerja Blender", value=2)

with col2:
    profit_Y = st.number_input("Keuntungan Per unit Pemanggang Roti (Rp)", value=8000)
    labor_Y = st.number_input("Jam kerja Pemanggang Roti", value=3)
    
# batasan
st.subheader("⛔ Batasan Waktu Mesin Per Minggu")
total_labor = st.slider("Total Jam Mesin Per Minggu (jam)", min_value=1, max_value=100, value=100, step=1)

# Tampilkan Fungsi Objektif
st.subheader("📈 Fungsi Objektif")

st.latex(r'''
\text Z = {%.0f}x + {%.0f}y
''' % (profit_X, profit_Y))

st.markdown("""
di mana:
- \\(x\\) = jumlah Blender
- \\(y\\) = jumlah Pemanggang Roti
""")

# Fungsi untuk download data sebagai JSON
def download_json(data, filename="hasil.json"):
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">📥 Download Hasil sebagai JSON</a>'
    return href

# Solve using linprog
c = [-profit_X, -profit_Y]  # Max profit -> Minimize negative
A = [[labor_X, labor_Y]]
b = [total_labor]

res = linprog(c, A_ub=A, b_ub=b, method='highs')

if res.success:
    x_blender, x_pemanggang_roti = res.x
    total_profit = -res.fun

    st.success("✅ Solusi Optimal Ditemukan!")
    st.write(f"Jumlah **Blender**: `{x_blender:.2f}` unit")
    st.write(f"Jumlah **Pemanggang Roti**: `{x_pemanggang_roti:.2f}` unit")
    st.write(f"💰 **Total Keuntungan Maksimal**: `Rp {total_profit:,.0f}`")

    # Tabel ringkasan
    hasil = pd.DataFrame({
        "Produk": ["Blender", "Pemanggang Roti"],
        "Jumlah Optimal": [x_blender, x_pemanggang_roti],
        "Keuntungan per Unit": [profit_X, profit_Y],
        "Total Keuntungan": [x_blender * profit_X, x_pemanggang_roti * profit_Y]
    })
    st.subheader("📋 Ringkasan Perhitungan")
    st.dataframe(hasil, use_container_width=True)

    # Download hasil
    st.markdown(download_json({
        "Blender": round(x_blender, 2),
        "Pemanggang Roti": round(x_pemanggang_roti, 2),
        "Total Keuntungan": round(total_profit, 2)
    }), unsafe_allow_html=True)

    # Visualisasi
    st.subheader("📊 Visualisasi Area Feasible dan Solusi Optimal")
    x_vals = np.linspace(0, 50, 400)
    y_vals = (total_labor - labor_X * x_vals) / labor_Y

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label='Batas Waktu Mesin', color='orange')
    ax.fill_between(x_vals, y_vals, 0, where=(y_vals >= 0), color='peachpuff', alpha=0.3)

    ax.plot(x_blender, x_pemanggang_roti, 'ro', label='Solusi Optimal')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Blender")
    ax.set_ylabel("Pemanggang Roti")
    ax.legend()
    st.pyplot(fig)

else:
    st.error("❌ Tidak ditemukan solusi feasible. Coba ubah batasan atau input.")
