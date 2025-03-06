import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
all_df = pd.read_csv("main_data.csv")

# Konversi kolom order_purchase_timestamp ke datetime
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# Membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal yang dipilih
main_df = all_df[
    (all_df["order_purchase_timestamp"].dt.date >= start_date) & 
    (all_df["order_purchase_timestamp"].dt.date <= end_date)
]

# Fungsi untuk membuat distribusi tipe pembayaran
def create_payment_distribution(df):
    payment = df["payment_type"].value_counts().reset_index()
    payment.columns = ["payment_type", "count"]
    return payment

# Fungsi untuk membuat performa penjualan per bulan
def create_monthly_orders(df):
    df["order_month"] = df["order_purchase_timestamp"].dt.month
    df["order_year"] = df["order_purchase_timestamp"].dt.year
    target_year = df["order_year"].max()
    orders = df[df["order_year"] == target_year].groupby("order_month").count()["order_id"].reset_index()
    return orders, target_year

payment_distribution = create_payment_distribution(main_df)
monthly_orders, target_year = create_monthly_orders(main_df)

# 1. Visualisasi Distribusi Tipe Pembayaran
st.subheader("Distribusi Tipe Pembayaran")
plt.figure(figsize=(10, 5))
sns.barplot(x="payment_type", y="count", data=payment_distribution)
plt.title("Distribusi Tipe Pembayaran", fontsize=15)
plt.xlabel("Tipe Pembayaran", fontsize=12)
plt.ylabel("Jumlah Transaksi", fontsize=12)
st.pyplot(plt)

# 2. Visualisasi Performa Penjualan Tiap Bulan
st.subheader(f"Performa Penjualan Tiap Bulan di Tahun {target_year}")
plt.figure(figsize=(10, 6))
sns.lineplot(x='order_month', y='order_id', data=monthly_orders, marker='o')
plt.title(f'Performa Penjualan Tiap Bulan di Tahun {target_year}')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Order')
plt.xticks(range(1, 13))
plt.grid(True)
st.pyplot(plt)
