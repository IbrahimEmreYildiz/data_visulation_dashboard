iimport streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

st.set_page_config(
    page_title="Life Style Data Analysis",
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Final_data.csv")

        if 'Age' in df.columns:
            df['Age'] = df['Age'].astype(int)

        cols_to_round = [
            'Experience_Level',
            'Workout_Frequency (days/week)',
            'Daily meals frequency',
            'Sets',
            'Reps'
        ]

        for col in cols_to_round:
            if col in df.columns:
                df[col] = df[col].round(0).astype(int)

        return df

    except FileNotFoundError:
        st.error("ERROR: 'Final_data.csv' file not found.")
        st.error("Please make sure 'Final_data.csv' is in the same folder as 'dashboard.py'.")
        return None


df = load_data()
if df is None:
    st.stop()


# -------------------- SIDEBAR -------------------- #

st.sidebar.header("Dashboard Filters")
st.sidebar.markdown("Filters here will affect all charts on the page.")

selected_genders = st.sidebar.multiselect(
    "Gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

selected_workouts = st.sidebar.multiselect(
    "Workout Type:",
    options=df['Workout_Type'].unique(),
    default=df['Workout_Type'].unique()
)

selected_diets = st.sidebar.multiselect(
    "Diet Type:",
    options=df['diet_type'].unique(),
    default=df['diet_type'].unique()
)

selected_difficulty = st.sidebar.multiselect(
    "Exercise Difficulty Level:",
    options=df['Difficulty Level'].unique(),
    default=df['Difficulty Level'].unique()
)

df_filtered = df[
    df['Gender'].isin(selected_genders) &
    df['Workout_Type'].isin(selected_workouts) &
    df['diet_type'].isin(selected_diets) &
    df['Difficulty Level'].isin(selected_difficulty)
]

if df_filtered.empty:
    st.warning("No data found for the selected filters. Please widen your selection.")
    st.stop()


# -------------------- HEADER -------------------- #

st.title("Life Style Data Analysis Dashboard")
st.markdown(
    f"**Dataset:** `Final_data.csv` | **Total Rows:** {len(df)} | **Filtered Rows:** {len(df_filtered)}"
)
st.markdown("---")


with st.expander("Show/Hide Filtered Data Sample (First 10 Rows)"):
    st.dataframe(df_filtered.head(10))

st.markdown("---")
st.header("Chart Section")


# -------------------- GRAPH 1 -------------------- #

st.subheader("Graph 1 (Medium, Grouped Bar Chart): Workout Type Distribution by Gender")
st.markdown("This chart updates dynamically based on the filters selected in the sidebar.")

chart_data_1 = df_filtered.groupby(['Gender', 'Workout_Type']).size().reset_index(name='count')

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


# -------------------- GRAPH 2 -------------------- #

st.subheader("Graph 2 (Advanced, Treemap): Exercise Distribution by Muscle Group and Difficulty")
st.markdown("This Treemap hierarchically shows which muscle groups are targeted most, broken down by difficulty.")

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


# -------------------- GRAPH 3 -------------------- #

st.subheader("Graph 3 (Advanced, Sankey Diagram): Flow from Diet Type to Workout Type")
st.markdown("This chart shows the flow of users between diet types and workout types. The thickness of the flow indicates the number of records.")

sankey_data = df_filtered.groupby(['diet_type', 'Workout_Type']).size().reset_index(name='count')

if sankey_data.empty:
    st.warning("No data found for Graph 3. Please widen your filters.")
else:

    all_labels = list(sankey_data['diet_type'].unique()) + list(sankey_data['Workout_Type'].unique())
    label_to_id = {label: i for i, label in enumerate(all_labels)}

    fig3 = go.Figure(
        data=[go.Sankey(
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
        )]
    )

    fig3.update_layout(
        title_text="Flow Between Diet Types and Workout Types",
        font_size=14,
        title_font_size=20
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# -------------------- GRAPH 4 -------------------- #

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


# -------------------- GRAPH 5 -------------------- #

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


# -------------------- GRAPH 6 -------------------- #

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


# -------------------- FOOTER -------------------- #

st.info("Remaining Charts: (2 Advanced, 1 Medium)")
