import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title='Bike Sharing Dashboard',
    layout='wide',
)

sns.set_theme(style='whitegrid')

DATA_PATH = Path(__file__).resolve().parent / 'main_data.csv'
SEASON_ORDER = ['Spring', 'Summer', 'Fall', 'Winter']


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header('Filter Data')

    years = sorted(df['year'].dropna().unique().tolist())
    selected_years = st.sidebar.multiselect('Tahun', options=years, default=years)

    available_seasons = [s for s in SEASON_ORDER if s in df['season_name'].unique()]
    selected_seasons = st.sidebar.multiselect('Musim', options=available_seasons, default=available_seasons)

    day_type = st.sidebar.radio(
        'Hari kerja / libur',
        options=['Semua', 'Hari Kerja', 'Libur/Akhir Pekan'],
        index=0,
    )

    filtered = df[df['year'].isin(selected_years) & df['season_name'].isin(selected_seasons)].copy()

    if day_type == 'Hari Kerja':
        filtered = filtered[filtered['workingday'] == 1]
    elif day_type == 'Libur/Akhir Pekan':
        filtered = filtered[filtered['workingday'] == 0]

    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    total_rentals = int(df['cnt'].sum())
    avg_rentals = float(df['cnt'].mean())
    peak_hour = int(df.groupby('hr')['cnt'].mean().idxmax())

    col1, col2, col3 = st.columns(3)
    col1.metric('Total Rentals', f"{total_rentals:,}")
    col2.metric('Average Rentals (per jam)', f"{avg_rentals:,.2f}")
    col3.metric('Peak Hour', f"{peak_hour:02d}:00")


def render_charts(df: pd.DataFrame) -> None:
    st.subheader('Tren Rental dari Waktu ke Waktu')
    daily_trend = df.groupby('dteday', as_index=False)['cnt'].sum()

    fig1, ax1 = plt.subplots(figsize=(12, 4))
    sns.lineplot(data=daily_trend, x='dteday', y='cnt', color='#1f77b4', ax=ax1)
    ax1.set_xlabel('Tanggal')
    ax1.set_ylabel('Total Rental')
    ax1.set_title('Total Rental Harian')
    st.pyplot(fig1, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader('Perbandingan Rental Berdasarkan Musim')
        season_data = (
            df.groupby('season_name', as_index=False)['cnt']
            .mean()
        )
        season_data['season_name'] = pd.Categorical(
            season_data['season_name'],
            categories=[s for s in SEASON_ORDER if s in season_data['season_name'].unique()],
            ordered=True,
        )
        season_data = season_data.sort_values('season_name')

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=season_data, x='season_name', y='cnt', palette='Blues_d', ax=ax2)
        ax2.set_xlabel('Musim')
        ax2.set_ylabel('Rata-rata Rental')
        ax2.set_title('Rata-rata Rental per Musim')
        st.pyplot(fig2, use_container_width=True)

    with col_right:
        st.subheader('Distribusi Penyewaan per Jam')
        hourly_data = df.groupby('hr', as_index=False)['cnt'].mean()

        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=hourly_data, x='hr', y='cnt', color='#4C72B0', ax=ax3)
        ax3.set_xlabel('Jam')
        ax3.set_ylabel('Rata-rata Rental')
        ax3.set_title('Rata-rata Rental per Jam')
        st.pyplot(fig3, use_container_width=True)


def main() -> None:
    st.title('Bike Sharing Data Analysis Dashboard')
    st.caption('Interaktif dashboard untuk memantau pola penyewaan sepeda berdasarkan waktu, musim, dan tipe hari.')

    df = load_data(DATA_PATH)
    filtered_df = apply_filters(df)

    if filtered_df.empty:
        st.warning('Data tidak tersedia untuk kombinasi filter yang dipilih.')
        st.stop()

    render_kpis(filtered_df)
    render_charts(filtered_df)


if __name__ == '__main__':
    main()
