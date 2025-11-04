import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------------
# SAYFA AYARI (Page Configuration)
# --------------------------------------------------------------------------------
# 'layout="wide"' dashboard'un tüm ekranı kaplamasını sağlar.
# Bu, 9 grafik göstereceğimiz için önemlidir.
st.set_page_config(
    page_title="Life Style Data Analizi",
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
        # Veri setini yüklüyoruz.
        df = pd.read_csv("Final_data.csv")
        return df
    except FileNotFoundError:
        # Eğer 'Final_data.csv' bulunamazsa hata verir.
        st.error("HATA: 'Final_data.csv' dosyası bulunamadı.")
        st.error("Lütfen 'Final_data.csv' dosyasının 'app.py' ile aynı klasörde olduğundan emin olun.")
        return None

# Veriyi 'df' değişkenine yüklüyoruz.
df = load_data()

# Eğer veri yüklenemediyse (hata verdiyse) uygulamayı durdur.
if df is None:
    st.stop()

# --------------------------------------------------------------------------------
# SIDEBAR (FİLTRE MENÜSÜ)
# --------------------------------------------------------------------------------
# Proje ödevi bizden en az 3 interaktif bileşen (filtre, slider vb.) istiyordu.
# Biz bunları sol taraftaki sidebar'a (yan menü) koyacağız.

st.sidebar.header("Dashboard Filtreleri")
st.sidebar.markdown("Buradaki filtreler tüm sayfadaki grafikleri etkileyecektir.")

# FİLTRE 1: Cinsiyet (Gender)
# 'multiselect' çoklu seçim yapmamızı sağlar.
# 'default=...' sayesinde başlangıçta tüm seçenekler seçili gelir.
selected_genders = st.sidebar.multiselect(
    "Cinsiyet (Gender):",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# FİLTRE 2: Antrenman Tipi (Workout Type)
selected_workouts = st.sidebar.multiselect(
    "Antrenman Tipi (Workout Type):",
    options=df['Workout_Type'].unique(),
    default=df['Workout_Type'].unique()
)

# FİLTRE 3: Diyet Tipi (Diet Type)
selected_diets = st.sidebar.multiselect(
    "Diyet Tipi (Diet Type):",
    options=df['diet_type'].unique(),
    default=df['diet_type'].unique()
)

# FİLTRE 4: Zorluk Seviyesi (Difficulty Level)
selected_difficulty = st.sidebar.multiselect(
    "Egzersiz Zorluk Seviyesi (Difficulty Level):",
    options=df['Difficulty Level'].unique(),
    default=df['Difficulty Level'].unique()
)

# --------------------------------------------------------------------------------
# FİLTRELENMİŞ VERİ (Filtered Data)
# --------------------------------------------------------------------------------
# Dashboard'un kalbi burası.
# Yukarıdaki sidebar'dan gelen seçimlere göre ana veri setimizi (df) filtreliyoruz.
# Örneğin, kullanıcı sadece 'Male' ve 'Cardio' seçerse, 'df_filtered' 
# sadece bu kişileri içeren bir alt küme haline gelir.
df_filtered = df[
    df['Gender'].isin(selected_genders) &
    df['Workout_Type'].isin(selected_workouts) &
    df['diet_type'].isin(selected_diets) &
    df['Difficulty Level'].isin(selected_difficulty)
]

# Eğer filtre sonucu hiç veri kalmazsa uyarı ver.
if df_filtered.empty:
    st.warning("Seçtiğiniz filtrelere uygun veri bulunamadı. Lütfen filtrelerinizi genişletin.")
    st.stop() # Veri yoksa uygulamayı burada durdur.

# --------------------------------------------------------------------------------
# ANA SAYFA (Main Page)
# --------------------------------------------------------------------------------

# Ana başlığımız.
st.title("Life Style Data Analizi Dashboard'u")
st.markdown(f"**Veri Seti:** `Final_data.csv` | **Toplam Satır:** {len(df)} | **Filtrelenmiş Satır:** {len(df_filtered)}")
st.markdown("---")

# --------------------------------------------------------------------------------
# GRAFİK ALANI (Chart Area)
# --------------------------------------------------------------------------------
# Şimdilik burası boş. 
# 9 grafiğimizi bu bölümün altına tek tek ekleyeceğiz.

st.header("Genel Bakış")

# Filtrelerin çalıştığını görmek için geçici olarak filtrelenmiş veriyi gösterelim.
st.markdown("### Filtrelenmiş Veri Örneği (Test amaçlı)")
st.dataframe(df_filtered.head())

st.markdown("---")
st.header("Grafik Bölümü (Yakında...)")
st.info("9 adet (6 Gelişmiş, 3 Orta) grafiğimiz buraya eklenecek.")