import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Setup awal halaman
st.title("Studi Kasus: Optimasi Produksi Pabrik")

st.markdown("""
## 📘 Studi Kasus
Sebuah pabrik memproduksi dua jenis produk:
- *Produk A (Blender)*: keuntungan Rp40.000/unit, waktu mesin 2 jam
- *Produk B (Pemanggang Roti)*: keuntungan Rp60.000/unit, waktu mesin 3 jam

*Total waktu mesin tersedia: 100 jam*

Tujuan: Tentukan jumlah masing-masing produk untuk *memaksimalkan keuntungan*.
""")

st.markdown("## 🔢 Langkah 1: Menentukan Variabel")
st.latex(r"x = \text{jumlah produk A (blender)}")
st.latex(r"y = \text{jumlah produk B (pemanggang roti)}")

st.markdown("## 🧮 Langkah 2: Menyusun Fungsi Objektif")
st.latex(r"Z = 40x + 60y")
st.write("Z adalah total keuntungan (dalam ribuan rupiah) yang ingin dimaksimalkan.")

st.markdown("## 📐 Langkah 3: Menyusun Kendala")
st.latex(r"2x + 3y \leq 100")
st.latex(r"x \geq 0, \quad y \geq 0")

st.write("Kendala ini berasal dari batasan waktu mesin maksimal 100 jam per minggu.")

st.markdown("## ✏ Langkah 4: Menyelesaikan Model (Metode Grafik)")

st.markdown("### Titik potong kendala:")
st.latex(r"x = 0 \Rightarrow 3y = 100 \Rightarrow y = 33.\overline{3}")
st.latex(r"y = 0 \Rightarrow 2x = 100 \Rightarrow x = 50")

st.markdown("### Uji Titik Pojok:")

# Hitung nilai Z pada titik-titik pojok
Z1 = 0
Z2 = 60 * 33.33
Z3 = 40 * 50

st.write(f"Titik (0, 0) ➜ Z = {Z1:,.0f} ribu")
st.write(f"Titik (0, 33.33) ➜ Z = {Z2:,.0f} ribu")
st.write(f"Titik (50, 0) ➜ Z = {Z3:,.0f} ribu")

st.markdown("## ✅ Solusi Optimal")

if Z2 >= Z3:
    st.success(f"Solusi optimal: Produksi 0 unit A dan 33 unit B ➜ Keuntungan maksimal Rp{Z2:,.0f} ribu")
else:
    st.success(f"Solusi optimal: Produksi 50 unit A dan 0 unit B ➜ Keuntungan maksimal Rp{Z3:,.0f} ribu")

st.markdown("### 🔍 Interpretasi:")
st.info("""
Perusahaan sebaiknya memilih satu jenis produksi secara penuh:
- Produksi 50 unit blender *atau*
- Produksi 33 unit pemanggang roti

Pilihlah berdasarkan permintaan pasar dan strategi penjualan.
""")
