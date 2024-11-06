# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

#impor data
hour_df = pd.read_csv("dashboard/hour_df_clean.csv")
#fungsi create jumlah penyewaan sepeda perhari
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    return daily_rent_df

#fungsi create rata-rata penyewaan per musim
def create_season_rent_df(df):
    season_rent_df = df.groupby(by="season").agg({
        "cnt": "mean"
    }).reset_index()
    return season_rent_df

#fungsi create rata-rata penyewaan per cuaca
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by="weathersit").agg({
        "cnt": "mean"
    }).reset_index()
    return weather_rent_df

#fungsi create rata-rata penyewaan per jam
def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby(by="hr").agg({
        "cnt": "mean"
    }).reset_index()

#fungsi create rata-rata penyewaan berdasarkan hari
def create_day_rent_df(df):
    day_rent_df = df.groupby(by="weekday").agg({
        "cnt": "mean"
    }).reset_index()
    return day_rent_df

#memastikan dteday bertipe data datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

#mengambil min dan max tanggal
min_date = hour_df['dteday'].min()
max_date = hour_df['dteday'].max()

with st.sidebar:
    #logo perusahaan (contoh)
    st.image("dashboard/sharing.png")
    #menambahkan widget rentang waktu
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#dataframe yang dijalankan
main_df = hour_df[(hour_df['dteday'] >= str(start_date)) & 
                  (hour_df['dteday'] <= str(end_date))]

#memanggil helper function
daily_rent_df = create_daily_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
hourly_rent_df = create_hourly_rent_df(main_df)
day_rent_df = create_day_rent_df(main_df)

st.header('Bike Sharing Dashboard :bike:')

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

#membuat tampilan poin penting pada daily_rent (jumlah hari, total dan rata-rata penyewaan)
with col1:
    total_days = daily_rent_df.shape[0]
    st.metric('Total Days', value=total_days)

with col2:
    daily_rent_df['cnt'].sum()
    st.metric('Total Rentals', value=round(daily_rent_df['cnt'].sum()))

with col3:
    daily_rent_df['cnt'].mean()
    st.metric('Average Rental Perday', value=round(daily_rent_df['cnt'].mean()))

#menampilkan line chart daily_rent berdasarkan main_df
fix, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df['dteday'],
    daily_rent_df['cnt'],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.grid(axis='y')

st.pyplot(fix)

#urutkan hari dari senin
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_rent_df['weekday'] = pd.Categorical(day_rent_df['weekday'], categories=day_order, ordered=True)

#menampilkan barchart rata rata penyewaan masing masing hari
st.subheader('Average Rents by Day')
fig, ax = plt.subplots(figsize=(24, 12))
sns.barplot(
    x='weekday',
    y='cnt',
    data=day_rent_df,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)

st.pyplot(fig)

#menampilkan kolom penyewaan by season dan by weather
st.subheader('Average Rent by Season and Rental')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))

sns.barplot(
    x='season',
    y='cnt',
    data=season_rent_df.sort_values(by='cnt', ascending=False),
    ax=ax1
)
ax1.set_title('Rents by Season', loc='center', fontsize=30)
ax1.set_ylabel(None)
ax1.tick_params(axis='x', labelsize=20)
ax1.tick_params(axis='y', labelsize=15)

sns.barplot(
    x='weathersit',
    y='cnt',
    data=weather_rent_df.sort_values(by='cnt', ascending=False),
    ax=ax2
)
ax2.set_title('Rents by Weather', loc='center', fontsize=30)
ax2.set_ylabel(None)
ax2.tick_params(axis='x', labelsize=20)
ax2.tick_params(axis='y', labelsize=15)

st.pyplot(fig)

