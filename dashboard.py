import streamlit as st # dashboard'un arayüzünü oluşturmak için
import pandas as pd # veri okuma ve işleme yapmak için
import plotly.express as px # grafik oluşturmak için
import plotly.graph_objects as go # advanced (gelişmiş grafikler için)


st.set_page_config( # sayfa ayarlarını düzenler streamlit kütüphanesinde tanımlı bir fonksiyon
    page_title="Life Style Data Analysis", # tarayıcıdaki başlık
    layout="wide" # sayfayı tüm ekrana yayar
)


@st.cache_data # veriyi önbellekleme demektir filtreler değiştiğinde zaman kaybetmemek için çok iyi bir kullanımdır
def load_data(): #veriyi yükleme fonksiyonu
    try:

        df = pd.read_csv("Final_data.csv")# pandas'ta veriyi dataframe(satır ve sütunlardan oluşan bir tablo) olarak yükler ve sonuç olarak tablo şekline dönüşür.

        if 'Age' in df.columns: # sütunlardaki age sütununun değerini floattan int yapar ki yaş değeri virgüllü olmasın diye
            df['Age'] = df['Age'].astype(int)

        cols_to_round = [ # bu da adından anlayacağımız üzere bu sütunları daha anlamlı olması için en yakın değere yuvarlar
            # örneğin bir insan spor salonunda 1.3 set hareket yapamaz veya haftada 3.2 gün spora gidemez
            'Experience_Level',
            'Workout_Frequency (days/week)',
            'Daily meals frequency',
            'Sets',
            'Reps',
            'Max_BPM',
            'Avg_BPM',

        ]

        for col in cols_to_round:
            if col in df.columns:

                df[col] = df[col].astype(float).round(0).astype(int) # burada round fonksiyonu "." dan sonra sayı olmasın anlamında bir pandas fonksiyonudur
                # yani önce yuvarla sonra integer yap yuvarlanınca 3.0 -> 3

        return df

    except FileNotFoundError: # data set yoksa hata verir

        st.error("ERROR: 'Final_data.csv' file not found.")
        st.error("Please make sure 'Final_data.csv' is in the same folder as 'dashboard.py'.")
        return None

df = load_data() #load_data () fonksiyonu çağrılıp df ye atanır eğer veri yoksa program durur.
if df is None:
    st.stop()


st.sidebar.header("Dashboard Filters")
st.sidebar.markdown("Filters here will affect all charts on the page.")


all_genders = df['Gender'].unique().tolist()
container_gender = st.sidebar.container()
select_all_gender = st.sidebar.checkbox("Select All Genders", value=True, key="gender_all")

if select_all_gender:
    selected_genders = container_gender.multiselect("Gender:", options=all_genders, default=all_genders)
else:
    selected_genders = container_gender.multiselect("Gender:", options=all_genders)


all_workouts = df['Workout_Type'].unique().tolist()
container_workout = st.sidebar.container()
select_all_workout = st.sidebar.checkbox("Select All Workout Types", value=True, key="workout_all")

if select_all_workout:
    selected_workouts = container_workout.multiselect("Workout Type:", options=all_workouts, default=all_workouts)
else:
    selected_workouts = container_workout.multiselect("Workout Type:", options=all_workouts)


all_diets = df['diet_type'].unique().tolist()
container_diet = st.sidebar.container()
select_all_diet = st.sidebar.checkbox("Select All Diet Types", value=True, key="diet_all")

if select_all_diet:
    selected_diets = container_diet.multiselect("Diet Type:", options=all_diets, default=all_diets)
else:
    selected_diets = container_diet.multiselect("Diet Type:", options=all_diets)


all_difficulties = df['Difficulty Level'].unique().tolist()
container_diff = st.sidebar.container()
select_all_diff = st.sidebar.checkbox("Select All Difficulty Levels", value=True, key="diff_all")

if select_all_diff:
    selected_difficulty = container_diff.multiselect("Exercise Difficulty Level:", options=all_difficulties, default=all_difficulties)
else:
    selected_difficulty = container_diff.multiselect("Exercise Difficulty Level:", options=all_difficulties)


all_muscles = df['Target Muscle Group'].unique().tolist()
container_muscle = st.sidebar.container()
select_all_muscle = st.sidebar.checkbox("Select All Muscle Groups", value=True, key="muscle_all")

if select_all_muscle:
    selected_muscles = container_muscle.multiselect("Target Muscle Group:", options=all_muscles, default=all_muscles)
else:
    selected_muscles = container_muscle.multiselect("Target Muscle Group:", options=all_muscles)


df_filtered = df[
    df['Gender'].isin(selected_genders) &
    df['Workout_Type'].isin(selected_workouts) &
    df['diet_type'].isin(selected_diets) &
    df['Difficulty Level'].isin(selected_difficulty) &
    df['Target Muscle Group'].isin(selected_muscles)
]


if df_filtered.empty: # seçili filtrelerle alakalı veri bulunamazsa uyarı
    st.warning("No data found for the selected filters. Please widen your selection.")
    st.stop()


st.title("Life Style Data Analysis Dashboard") # sayfanın grafiklerinin üstündeki ana başlık
st.markdown(
    f"**Dataset:** `Final_data.csv` | **Total Rows:** {len(df)} | **Filtered Rows:** {len(df_filtered)}")
st.markdown("---")


with st.expander("Show/Hide Filtered Data Sample (First 20 Rows)"): # filtrelenen veriler çok fazla olursa ilk 10 satırını gösterir.
    st.dataframe(df_filtered.head(20))

st.markdown("---")
st.header("Chart Section")

#chartın başlığı
st.subheader("Graph 1 (Medium, Grouped Bar Chart): Workout Type Distribution by Gender")
st.markdown("This chart updates dynamically based on the filters selected in the sidebar.")


chart_data_1 = df_filtered.groupby(['Gender', 'Workout_Type']).size().reset_index(name='count') # filtrelenmiş verileri gruplar

if chart_data_1.empty:
    st.warning("No data found for Graph 1. Please widen your filters.")
else:

    fig1 = px.bar(
        chart_data_1,
        x='Gender',
        y='count',
        color='Workout_Type',
        barmode='group',
        title='Workout Type Distribution by Gender',
        labels={'count': 'Record Count', 'Gender': 'Gender', 'Workout_Type': 'Workout Type'}
    )

    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")


st.subheader("Graph 2 (Advanced, Treemap): Exercise Distribution by Muscle Group and Difficulty")
st.markdown(
    "This Treemap hierarchically shows which muscle groups are targeted most, broken down by difficulty.")

chart_data_2 = df_filtered.groupby(['Difficulty Level', 'Target Muscle Group']).size().reset_index(name='count')

if chart_data_2.empty:
    st.warning("No data found for Graph 2. Please widen your filters.")
else:

    fig2 = px.treemap(
        chart_data_2,
        path=[px.Constant("All Exercises"), 'Difficulty Level', 'Target Muscle Group'],
        values='count',
        color='Difficulty Level',
        title='Hierarchical Distribution: Difficulty Level and Target Muscle Groups',
        hover_data={'Difficulty Level': False, 'count': True},
        labels={'count': 'Record Count', 'Target Muscle Group': 'Target Muscle Group'}
    )

    fig2.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        font_size=16,
        title_font_size=20
    )

    fig2.update_traces(textfont_size=14)

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


st.subheader("Graph 3 (Advanced, Sankey Diagram): Flow from Diet Type to Workout Type")
st.markdown(
    "This chart shows the flow of users between diet types and workout types. The thickness of the flow indicates the number of records.")

sankey_data = df_filtered.groupby(['diet_type', 'Workout_Type']).size().reset_index(name='count')

if sankey_data.empty:
    st.warning("No data found for Graph 3. Please widen your filters.")
else:

    all_labels = list(sankey_data['diet_type'].unique()) + list(sankey_data['Workout_Type'].unique())

    label_to_id = {label: i for i, label in enumerate(all_labels)}

    fig3 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color="blue"
        ),

        link=dict(
            source=sankey_data['diet_type'].map(label_to_id),
            target=sankey_data['Workout_Type'].map(label_to_id),
            value=sankey_data['count']
        )
    )])

    fig3.update_layout(
        title_text="Flow Between Diet Types and Workout Types",
        font_size=14,
        title_font_size=20
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

#------------------------------------------------İBRAHİM EMRE YILDIZ-----------------------------------------------------


st.subheader("Graph 4 (Medium, Line Chart): Average BPM Across Age")
st.markdown("This line chart shows how the average BPM varies by age.")

line_data = df_filtered.groupby("Age")["Avg_BPM"].mean().reset_index()

if line_data.empty:
    st.warning("No data found for Graph 4. Please widen your filters.")
else:
    fig4 = px.line(
        line_data,
        x="Age",
        y="Avg_BPM",
        markers=True,
        title="Average BPM by Age",
        labels={"Avg_BPM": "Average BPM", "Age": "Age"}
    )
    st.plotly_chart(fig4, use_container_width=True)


st.markdown("---")

st.subheader("Graph 5 (Advanced, Scatter Plot): Max BPM vs Average BPM")
st.markdown("This scatter plot compares Max BPM and Average BPM.")

scatter_data = df_filtered[["Max_BPM", "Avg_BPM"]].dropna()

if scatter_data.empty:
    st.warning("No data found for Graph 5. Please widen your filters.")
else:
    fig5 = px.scatter(
        scatter_data,
        x="Avg_BPM",
        y="Max_BPM",
        trendline="ols",
        title="Scatter Plot: Max BPM vs Average BPM",
        labels={"Avg_BPM": "Average BPM", "Max_BPM": "Max BPM"}
    )
    st.plotly_chart(fig5, use_container_width=True)


st.markdown("---")

st.subheader("Graph 6 (Advanced, Sunburst Chart): Diet → Workout → Difficulty Breakdown")
st.markdown("This hierarchical sunburst chart shows how diet types relate to workout types and difficulty levels.")

sunburst_data = df_filtered.groupby(
    ["diet_type", "Workout_Type", "Difficulty Level"]
).size().reset_index(name="count")

if sunburst_data.empty:
    st.warning("No data found for Graph 6. Please widen your filters.")
else:
    fig6 = px.sunburst(
        sunburst_data,
        path=["diet_type", "Workout_Type", "Difficulty Level"],
        values="count",
        color="diet_type",
        title="Sunburst Breakdown of Diet → Workout → Difficulty",
        maxdepth=-1
    )

    fig6.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        title_font_size=20
    )

    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

#-----------------------------------------------------KAMAL ASADOV------------------------------------------------------
st.subheader("Graph 7 (Advanced, Density Plot): Age Density by Gender")
st.markdown("This chart updates dynamically based on the filters selected in the sidebar.")


# Veriyi hazırlıyoruz, sadece Yaş ve Cinsiyet lazım
chart_data_density = df_filtered[['Age', 'Gender']].dropna()

if chart_data_density.empty:
    st.warning("No data found for Density Plot. Please widen your filters.")
else:
    # 1. RENK ÇÖZÜMÜ: Renkleri kesin olarak atıyoruz. Kırmızı ve Mavi.
    color_map = {'Male': '#1f77b4', 'Female': '#d62728'} # Mavi ve Kırmızı kodları

    fig_density = px.histogram(
        chart_data_density,
        x="Age",
        color="Gender",
        color_discrete_map=color_map, # Renk haritamızı buraya ekledik
        histnorm='probability density', # Çubuk yerine pürüzsüz eğri (density curve) çizmesini sağlar
        title="Age Distribution Density by Gender (Smooth Curves)",
        barmode="overlay", # Erkek ve kadın grafikleri üst üste binsin
        opacity=0.6 # Saydamlık ekle ki üst üste binen yerler görünsün
    )

    # Grafiğin genel görünüm ayarları
    fig_density.update_layout(
        xaxis_title="Age",
        yaxis_title="Density (Yoğunluk)",
        legend=dict(
            orientation="h", # Lejantı yatay yap
            yanchor="bottom",
            y=1.02, # Grafiğin üstüne al
            xanchor="right",
            x=1,
            title=None # 'Gender' başlığını kaldır, daha temiz dursun
        ),
        margin=dict(l=20, r=20, t=50, b=20) # Kenar boşluklarını ayarla
    )

    st.plotly_chart(fig_density, use_container_width=True)

st.markdown("---")


st.subheader("Graph 8 (Advanced, Box Plot): Session Duration by Workout Type")
st.markdown("This box plot compares session durations across different workout types. It updates based on filters in the sidebar.")

chart_data_B = df_filtered[['Workout_Type', 'Session_Duration (hours)']].dropna()

if chart_data_B.empty:
    st.warning("No data found for Graph B. Please widen your filters.")
else:
    figB = px.box(
        chart_data_B,
        x='Workout_Type',
        y='Session_Duration (hours)',
        title='Session Duration by Workout Type',
        labels={'Workout_Type': 'Workout Type', 'Session_Duration (hours)': 'Duration (hours)'}
    )

    st.plotly_chart(figB, use_container_width=True)

st.markdown("---")


st.subheader("Graph 9 (Medium, Histogram): Distribution of Max BPM")
st.markdown("This histogram shows the distribution of maximum heart rate values among filtered records.")

chart_data_C = df_filtered[['Max_BPM']].dropna()

if chart_data_C.empty:
    st.warning("No data found for Graph 9. Please widen your filters.")
else:
    figC = px.histogram(
        chart_data_C,
        x='Max_BPM',
        nbins=30,
        title='Distribution of Max BPM',
        labels={'Max_BPM': 'Max BPM'}
    )

    st.plotly_chart(figC, use_container_width=True)

st.markdown("---")


#------------------------------------------------------MUHLİS ÇOLAK--------------------------------------------------
