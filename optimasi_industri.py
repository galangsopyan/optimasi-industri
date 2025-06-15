import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Model Matematika Industri", layout="wide")
st.title("📊 Aplikasi Model Matematika untuk Industri")

# Tab
tab1, tab2, tab3, tab4 = st.tabs(["Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Tambahan"])

# Tab 1: Optimasi Produksi
with tab1:
    st.header("🔧 Optimasi Produksi - Linear Programming")
    st.markdown("Masukkan fungsi tujuan dan kendala dalam bentuk koefisien.")

    c = st.text_input("Koefisien Fungsi Tujuan (misal: -3, -5)", "-3, -5")
    A = st.text_area("Matriks Kendala A (pisahkan baris dengan enter)", "1, 0\n0, 2\n3, 2")
    b = st.text_input("RHS Kendala (misal: 4, 12, 18)", "4, 12, 18")

    if st.button("Hitung Optimasi"):
        c = list(map(float, c.split(',')))
        A = [list(map(float, row.split(','))) for row in A.strip().split('\n')]
        b = list(map(float, b.split(',')))

        res = linprog(c, A_ub=A, b_ub=b, method='highs')
        if res.success:
            st.success(f"Nilai optimal: {res.fun:.2f}, Variabel: {res.x}")
        else:
            st.error("Gagal menyelesaikan optimasi.")

# Tab 2: Model EOQ
with tab2:
    st.header("📦 Model Persediaan EOQ")
    D = st.number_input("Permintaan tahunan (D)", value=1000)
    S = st.number_input("Biaya pemesanan per pesanan (S)", value=50.0)
    H = st.number_input("Biaya penyimpanan per unit per tahun (H)", value=5.0)

    if st.button("Hitung EOQ"):
        eoq = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ (Economic Order Quantity) = {eoq:.2f} unit")

# Tab 3: Model Antrian M/M/1
with tab3:
    st.header("⏳ Model Antrian M/M/1")
    lam = st.number_input("Laju kedatangan λ (per menit)", value=2.0)
    mu = st.number_input("Laju pelayanan μ (per menit)", value=3.0)

    if st.button("Hitung Antrian"):
        if lam >= mu:
            st.error("Sistem tidak stabil (λ ≥ μ)")
        else:
            rho = lam / mu
            L = rho / (1 - rho)
            Lq = rho**2 / (1 - rho)
            W = 1 / (mu - lam)
            Wq = lam / (mu * (mu - lam))
            st.write(f"Rho (ρ): {rho:.2f}")
            st.write(f"Rata-rata dalam sistem (L): {L:.2f}")
            st.write(f"Rata-rata dalam antrian (Lq): {Lq:.2f}")
            st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f} menit")
            st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f} menit")

# Tab 4: Model Matematika Lain
with tab4:
    st.header("🧮 Model Tambahan: Break-Even Point")
    FC = st.number_input("Biaya Tetap (Fixed Cost)", value=10000.0)
    VC = st.number_input("Biaya Variabel per Unit (Variable Cost)", value=20.0)
    P = st.number_input("Harga Jual per Unit (Price)", value=50.0)

    if st.button("Hitung Break-Even Point"):
        if P > VC:
            BEP = FC / (P - VC)
            st.success(f"Break-Even Point: {BEP:.2f} unit")
        else:
            st.error("Harga jual harus lebih besar dari biaya variabel.")
