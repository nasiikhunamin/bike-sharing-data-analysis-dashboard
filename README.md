# Proyek Analisis Data Bike Sharing Dataset

## Deskripsi Proyek
Proyek ini merupakan analisis data end-to-end pada Bike Sharing Dataset (2011-2012) menggunakan Python. Analisis dilakukan dari tahap data wrangling, exploratory data analysis (EDA), visualisasi, hingga analisis lanjutan manual clustering/binning demand. Hasil analisis kemudian disajikan dalam dashboard interaktif berbasis Streamlit.

## Tujuan Analisis
1. Memahami pengaruh musim dan kondisi cuaca terhadap jumlah penyewaan sepeda.
2. Mengidentifikasi waktu (jam) dengan tingkat penyewaan tertinggi.
3. Membandingkan pola penyewaan pada hari kerja vs hari libur/akhir pekan.
4. Membuat segmentasi demand (low, medium, high) untuk mendukung keputusan operasional.

## Insight Utama
- Permintaan tertinggi terjadi pada musim Fall dan Summer.
- Cuaca cerah (Clear) menghasilkan rata-rata penyewaan tertinggi dibanding cuaca buruk.
- Jam puncak berada di sore hari (sekitar pukul 17:00), terutama pada hari kerja.
- Segmentasi manual demand membantu memisahkan periode low/medium/high demand untuk kebutuhan perencanaan kapasitas.

## Struktur Folder
```text
bike-sharing-data-analysis-dashboard/
|-- dashboard/
|   |-- dashboard.py
|   `-- main_data.csv
|-- data/
|   |-- day.csv
|   `-- hour.csv
|-- notebook.ipynb
|-- README.md
|-- requirements.txt
```

## Menjalankan Dashboard Secara Lokal
1. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan Streamlit:
   ```bash
   streamlit run dashboard/dashboard.py
   ```

## Catatan
- Notebook analisis utama berada pada file `notebook.ipynb`.
- File `url.txt` dikosongkan karena deployment Streamlit Cloud belum dilakukan.
