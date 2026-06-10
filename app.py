import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Data Dashboard", page_icon="📊", layout="wide")

st.title("📊 Data Dashboard")
st.markdown("Dashboard interaktif untuk eksplorasi `DATASET.xlsx`.")

# Load Data
@st.cache_data
def load_data():
    file_path = "DATASET.xlsx"
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            # Konversi kolom yang mungkin berupa angka (tapi terbaca sebagai teks) menjadi numerik
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            
            # Pastikan kolom tipe campuran diubah menjadi string agar tidak error di Streamlit (PyArrow)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str)
            return df
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        st.error(f"File '{file_path}' not found in the current directory.")
        return None

df = load_data()

if df is not None and not df.empty:
    st.sidebar.header("Filter Data")
    
    # Menampilkan Raw Data
    st.subheader("📋 Raw Data & Summary")
    with st.expander("Tampilkan Raw Data"):
        st.dataframe(df)
        
    with st.expander("Tampilkan Summary Statistics"):
        st.write(df.describe(include='all').T)

    st.divider()

    st.subheader("📈 Visualisasi Data")
    
    # Deteksi kolom numerik dan kategorikal
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=['float64', 'int64']).columns.tolist()

    if numeric_columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Bar Chart")
            bar_x = st.selectbox("Pilih Kolom X (Bar)", options=df.columns, key='bar_x')
            bar_y = st.selectbox("Pilih Kolom Y (Bar - Numerik)", options=numeric_columns, key='bar_y')
            if st.button("Buat Bar Chart"):
                fig_bar = px.bar(df, x=bar_x, y=bar_y, title=f"Bar Chart: {bar_y} per {bar_x}")
                st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.markdown("### 📉 Line Chart")
            line_x = st.selectbox("Pilih Kolom X (Line)", options=df.columns, key='line_x')
            line_y = st.selectbox("Pilih Kolom Y (Line - Numerik)", options=numeric_columns, key='line_y')
            if st.button("Buat Line Chart"):
                # Urutkan data berdasarkan X untuk line chart yang lebih rapi
                df_sorted = df.sort_values(by=line_x)
                fig_line = px.line(df_sorted, x=line_x, y=line_y, title=f"Line Chart: {line_y} per {line_x}")
                st.plotly_chart(fig_line, use_container_width=True)
                
        st.divider()
        
        st.markdown("### 🔍 Scatter Plot")
        scat_x = st.selectbox("Pilih Kolom X (Numerik)", options=numeric_columns, key='scat_x')
        scat_y = st.selectbox("Pilih Kolom Y (Numerik)", options=numeric_columns, key='scat_y')
        scat_color = st.selectbox("Pilih Warna Berdasarkan (Opsional)", options=["None"] + categorical_columns, key='scat_color')
        
        if st.button("Buat Scatter Plot"):
            color_arg = None if scat_color == "None" else scat_color
            fig_scatter = px.scatter(df, x=scat_x, y=scat_y, color=color_arg, title=f"Scatter Plot: {scat_y} vs {scat_x}")
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Tidak ada kolom numerik yang ditemukan untuk divisualisasikan.")

else:
    st.warning("Data kosong atau belum tersedia.")
