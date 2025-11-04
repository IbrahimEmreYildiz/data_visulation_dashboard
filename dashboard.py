import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # <-- YENİ EKLENEN SATIR (Sankey için)
# --------------------------------------------------------------------------------
# SAYFA AYARI (Page Configuration)
# --------------------------------------------------------------------------------
# 'layout="wide"' dashboard'un tüm ekranı kaplamasını sağlar.
# Bu, 9 grafik göstereceğimiz için önemlidir.
st.set_page_config(
    page_title="Life Style Data Analysis", # <- DEĞİŞTİ (İNGİLİZCE)
    layout="wide"
)

# --------------------------------------------------------------------------------
# VERİ YÜKLEME (Data Loading)
# --------------------------------------------------------------------------------
# '@st.cache_data' Streamlit'e özel bir komuttur.
# 20.000 satırlık veriyi her filtreye tıkladığında tekrar tekrar yüklemez.
# Veriyi hafızaya alır ve dashboard'u AŞIRI hızlı çalıştırır.
# Bu, projen için kritik bir optimizasyondur.
@st.cache_data
def load_data():
    try:
        # Load the dataset
        df = pd.read_csv("Final_data.csv")

        # ----------------------------------------------------------------
        # DATA PREPROCESSING (As requested in Assignment Item 2)
        # ----------------------------------------------------------------

        # 1. Convert 'Age' to integer (e.g., 34.91 -> 34)
        if 'Age' in df.columns:
            df['Age'] = df['Age'].astype(int)

        # 2. Round other nonsensical float columns to the nearest integer
        #    (e.g., 3.99 -> 4, 4.99 -> 5, 20.91 -> 21)
        cols_to_round = [
            'Experience_Level',
            'Workout_Frequency (days/week)',
            'Daily meals frequency',
            'Sets',
            'Reps'
        ]

        for col in cols_to_round:
            if col in df.columns:
                # First round to nearest integer (e.g., 3.99 -> 4.0)
                # Then convert to integer type (e.g., 4.0 -> 4)
                df[col] = df[col].round(0).astype(int)
        # ----------------------------------------------------------------

        return df

    except FileNotFoundError:
        # Error message in English
        st.error("ERROR: 'Final_data.csv' file not found.")
        st.error("Please make sure 'Final_data.csv' is in the same folder as 'dashboard.py'.")
        return None

# Veriyi 'df' değişkenine yüklüyoruz.
# Load data into 'df'
df = load_data()

# If data loading failed, stop the app
if df is None:
    st.stop()

# --------------------------------------------------------------------------------
# SIDEBAR (FILTER MENU)
# --------------------------------------------------------------------------------
# (All labels changed to English)

st.sidebar.header("Dashboard Filters")
st.sidebar.markdown("Filters here will affect all charts on the page.")

# FILTER 1: Gender
selected_genders = st.sidebar.multiselect(
    "Gender:",  # <- DEĞİŞTİ
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# FILTER 2: Workout Type
selected_workouts = st.sidebar.multiselect(
    "Workout Type:",  # <- DEĞİŞTİ
    options=df['Workout_Type'].unique(),
    default=df['Workout_Type'].unique()
)

# FILTER 3: Diet Type
selected_diets = st.sidebar.multiselect(
    "Diet Type:",  # <- DEĞİŞTİ
    options=df['diet_type'].unique(),
    default=df['diet_type'].unique()
)

# FILTER 4: Difficulty Level
selected_difficulty = st.sidebar.multiselect(
    "Exercise Difficulty Level:",  # <- DEĞİŞTİ
    options=df['Difficulty Level'].unique(),
    default=df['Difficulty Level'].unique()
)

# --------------------------------------------------------------------------------
# FILTERED DATAFRAME
# --------------------------------------------------------------------------------
# Create the filtered dataframe based on sidebar selections
df_filtered = df[
    df['Gender'].isin(selected_genders) &
    df['Workout_Type'].isin(selected_workouts) &
    df['diet_type'].isin(selected_diets) &
    df['Difficulty Level'].isin(selected_difficulty)
    ]

# Warning if filters result in no data
if df_filtered.empty:
    st.warning("No data found for the selected filters. Please widen your selection.")  # <- DEĞİŞTİ
    st.stop()  # Stop the app if no data

# --------------------------------------------------------------------------------
# MAIN PAGE
# --------------------------------------------------------------------------------

# Main title in English
st.title("Life Style Data Analysis Dashboard")  # <- DEĞİŞTİ
st.markdown(
    f"**Dataset:** `Final_data.csv` | **Total Rows:** {len(df)} | **Filtered Rows:** {len(df_filtered)}")  # <- DEĞİŞTİ
st.markdown("---")

# Expander for raw data view (in English)
with st.expander("Show/Hide Filtered Data Sample (First 10 Rows)"):  # <- DEĞİŞTİ
    st.dataframe(df_filtered.head(10))

st.markdown("---")
st.header("Chart Section")  # <- DEĞİŞTİ

# --------------------------------------------------------------------------------
# CHART 1 (Medium): Workout Type Distribution by Gender
# --------------------------------------------------------------------------------
st.subheader("Graph 1 (Medium): Workout Type Distribution by Gender")  # <- DEĞİŞTİ
st.markdown("This chart updates dynamically based on the filters selected in the sidebar.")  # <- DEĞİŞTİ

# 1. Prepare data for Chart 1
chart_data_1 = df_filtered.groupby(['Gender', 'Workout_Type']).size().reset_index(name='count')

if chart_data_1.empty:
    st.warning("No data found for Graph 1. Please widen your filters.")  # <- DEĞİŞTİ
else:
    # 2. Draw Chart 1 (Plotly)
    fig1 = px.bar(
        chart_data_1,
        x='Gender',
        y='count',
        color='Workout_Type',
        barmode='group',
        title='Workout Type Distribution by Gender',  # <- DEĞİŞTİ
        labels={'count': 'Record Count', 'Gender': 'Gender', 'Workout_Type': 'Workout Type'}  # <- DEĞİŞTİ
    )

    # 3. Display Chart 1 in Streamlit
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")  # Separator line

# --------------------------------------------------------------------------------
# CHART 2 (Advanced): Exercise Distribution by Muscle Group (Treemap)
# --------------------------------------------------------------------------------
st.subheader("Graph 2 (Advanced): Exercise Distribution by Muscle Group and Difficulty")  # <- DEĞİŞTİ
st.markdown(
    "This Treemap hierarchically shows which muscle groups are targeted most, broken down by difficulty.")  # <- DEĞİŞTİ

# 1. Prepare data for Chart 2
chart_data_2 = df_filtered.groupby(['Difficulty Level', 'Target Muscle Group']).size().reset_index(name='count')

if chart_data_2.empty:
    st.warning("No data found for Graph 2. Please widen your filters.")  # <- DEĞİŞTİ
else:
    # 2. Draw Chart 2 (Plotly)
    fig2 = px.treemap(
        chart_data_2,
        path=[px.Constant("All Exercises"), 'Difficulty Level', 'Target Muscle Group'],  # <- DEĞİŞTİ
        values='count',
        color='Difficulty Level',
        title='Hierarchical Distribution: Difficulty Level and Target Muscle Groups',  # <- DEĞİŞTİ
        hover_data={'Difficulty Level': False, 'count': True},
        labels={'count': 'Record Count', 'Target Muscle Group': 'Target Muscle Group'}  # <- DEĞİŞTİ
    )

    # --- YAZI TİPİ VE KENAR BOŞLUĞU AYARI (GÜNCELLENDİ) ---
    # Hem kenar boşluklarını hem de yazı tiplerini ayarlıyoruz
    fig2.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),  # Kenar boşlukları (bu zaten vardı)
        font_size=16,  # Genel font boyutu (Başlık, yol çubuğu vb.)
        title_font_size=20  # Ana başlık
    )

    # Treemap'in İÇİNDEKİ etiketlerin (kas grubu isimleri) boyutunu ayarla
    # (Bunu 'update_traces' ile yapmamız gerekiyor)
    fig2.update_traces(
        textfont_size=14  # İç etiketleri çok büyük yaparsak kutulara sığmaz
    )
    # ----------------------------------------------------

    # 3. Display Chart 2 in Streamlit
    st.plotly_chart(fig2, use_container_width=True)

# ... (Grafik 2'nin st.plotly_chart(fig2, ...) satırı burada bitmiş olmalı) ...

st.markdown("---")  # Grafikler arasına ayırıcı bir çizgi koyalım

# --------------------------------------------------------------------------------
# GRAFİK 3 (Gelişmiş Seviye): Diyet Tipi -> Antrenman Tipi Akışı (Sankey Diagram)
# (Paralel Koordinatlar grafiğinin yerine eklendi - daha anlaşılır)
# --------------------------------------------------------------------------------
st.subheader("Graph 3 (Advanced): Flow from Diet Type to Workout Type (Sankey)")
st.markdown(
    "This chart shows the flow of users between diet types and workout types. The thickness of the flow indicates the number of records.")

# 1. Veriyi Hazırlama (Sankey için bu kısım karmaşıktır):
#    Akışı 'diet_type' -> 'Workout_Type' olarak belirleyip sayımlarını alıyoruz.
sankey_data = df_filtered.groupby(['diet_type', 'Workout_Type']).size().reset_index(name='count')

if sankey_data.empty:
    st.warning("No data found for Graph 3. Please widen your filters.")
else:
    # Sankey grafiği metin ('HIIT', 'Vegan') kabul etmez, sayısal ID'ler ister (0, 1, 2...).
    # Bu yüzden tüm etiketler (hem diyet hem antrenman) için bir liste oluşturmalıyız.
    all_labels = list(sankey_data['diet_type'].unique()) + list(sankey_data['Workout_Type'].unique())

    # Etiketleri sayısal ID'lere çevirmek için bir sözlük (map) oluşturuyoruz
    # (örn: 'Vegan': 0, 'Paleo': 1, 'Cardio': 2, 'HIIT': 3 ...)
    label_to_id = {label: i for i, label in enumerate(all_labels)}

    # 2. Grafiği Çizme (Plotly Graph Objects - 'go' ile):
    fig3 = go.Figure(data=[go.Sankey(
        # Düğümler (Nodes): Kategorilerin (Diyetler, Antrenmanlar) kendisi
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,  # Düğümlerin isimleri (örn: 'Vegan', 'Paleo', 'Cardio'...)
            color="blue"  # Düğümlerin rengi
        ),
        # Bağlantılar (Links): Akışın kendisi (Diyet -> Antrenman)
        link=dict(
            # 'source' (kaynak) listesi (diyet tiplerinin sayısal ID'leri)
            source=sankey_data['diet_type'].map(label_to_id),

            # 'target' (hedef) listesi (antrenman tiplerinin sayısal ID'leri)
            target=sankey_data['Workout_Type'].map(label_to_id),

            # 'value' (değer) listesi (akışın kalınlığı, yani 'count')
            value=sankey_data['count']
        ))])

    # 3. Grafik Başlığını ve Yazı Tiplerini Ayarlama:
    fig3.update_layout(
        title_text="Flow Between Diet Types and Workout Types",
        font_size=14,  # Yazı tipini okunaklı yap
        title_font_size=20
    )

    # 4. Grafiği Streamlit'e Basma:
    st.plotly_chart(fig3, use_container_width=True)

# Kalan grafik sayısını güncelleyelim (Sayı değişmedi, sadece grafik tipi değişti)
st.info("Remaining Charts: 6 (4 Advanced, 2 Medium)")

