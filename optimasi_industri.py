import streamlit as st
from scipy.optimize import linprog
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Optimasi Produksi - PT. Sinar Terang", layout="centered")
st.title("🏭 Optimasi Produksi - PT. Sinar Terang")

st.markdown("""
Aplikasi ini membantu PT. Sinar Terang menentukan jumlah produksi optimal untuk dua produk:
- Produk A: Blender
- Produk B: Pemanggang Roti

Tujuannya adalah untuk memaksimalkan keuntungan, dengan batasan waktu mesin yang tersedia per minggu.
""")

with st.form("input_form"):
    st.subheader("🔧 Masukkan Parameter Produksi")

    col1, col2 = st.columns(2)

    with col1:
        profit_A = st.number_input("Keuntungan per unit Blender (Rp)", value=40000, step=1000, min_value=0)
        time_A = st.number_input("Jam mesin per unit Blender", value=2.0, step=0.1, min_value=0.1)
    
    with col2:
        profit_B = st.number_input("Keuntungan per unit Pemanggang Roti (Rp)", value=60000, step=1000, min_value=0)
        time_B = st.number_input("Jam mesin per unit Pemanggang Roti", value=3.0, step=0.1, min_value=0.1)
    
    total_time = st.number_input("Total jam mesin tersedia per minggu", value=100.0, step=1.0, min_value=1.0)
    
     # Tambahan baru: Menampilkan rumus fungsi tujuan
     st.markdown("### 📈 Fungsi Tujuan:")
     st.latex(f"Z = {profit_A}x + {profit_B}y")

    submitted = st.form_submit_button("🔍 Hitung Produksi Optimal")



if submitted:
    c = [-profit_A, -profit_B]
    A = [[time_A, time_B]]
    b = [total_time]
    bounds = [(0, None), (0, None)]

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    st.subheader("📊 Hasil Optimasi")

    if result.success:
        x = result.x[0]
        y = result.x[1]
        max_profit = -result.fun

        st.success("Solusi optimal ditemukan ✅")
        st.write(f"🔹 Jumlah Blender (Produk A): **{x:.2f} unit**")
        st.write(f"🔹 Jumlah Pemanggang Roti (Produk B): **{y:.2f} unit**")
        st.write(f"💰 Total keuntungan maksimal: Rp {max_profit:,.0f}")

        # ===== VISUALISASI =====
        st.subheader("📉 Visualisasi Daerah Solusi & Titik Optimal")

        fig, ax = plt.subplots(figsize=(7, 5))

        x_vals = np.linspace(0, total_time / time_A + 5, 400)
        y_vals = (total_time - time_A * x_vals) / time_B
        y_vals = np.maximum(0, y_vals)

        ax.plot(x_vals, y_vals, label="Batas Waktu Mesin", color="blue")
        ax.fill_between(x_vals, 0, y_vals, alpha=0.2, color="blue", label="Daerah Feasible")

        ax.scatter(x, y, color="red", zorder=5, label="Solusi Optimal")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("Unit Blender (Produk A)")
        ax.set_ylabel("Unit Pemanggang Roti (Produk B)")
        ax.set_title("Visualisasi Optimasi Produksi")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    else:
        st.error("❌ Gagal menemukan solusi optimal.")
