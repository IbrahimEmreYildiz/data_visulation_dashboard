# 🏋️ Gym & Fitness Lifestyle Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Data Scale](https://img.shields.io/badge/Data-20k_Rows-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **CEN445 - Introduction to Data Visualization Course Project (Fall 2025)**
>
> *An interactive, data-driven dashboard exploring the intersection of nutritional habits, workout intensity, and physiological health using a large-scale dataset.*

---

## 📑 Table of Contents
1. [Dataset Details](#-dataset-details)
2. [Dashboard Preview](#-dashboard-preview)
3. [Team & Roles](#-team--roles)
4. [Technical Architecture](#-technical-architecture)
5. [Key Insights](#-key-insights)
6. [Installation Guide](#-installation-guide)
7. [Future Roadmap](#-future-roadmap)

---

## 📌 Project Overview
In the modern fitness landscape, data plays a pivotal role in optimizing performance. This project leverages the **Gym Members Exercise Dataset** to visualize complex correlations between lifestyle choices and health outcomes.

**Core Objectives:**
* **Analyze** the impact of diet types (e.g., Paleo, Vegan) on workout preferences.
* **Visualize** demographic clusters to understand gym engagement trends.
* **Correlate** physiological metrics (Heart Rate, BMI) with exercise intensity and experience levels.

---

## 📂 Dataset Details
We utilized a high-dimensional dataset significantly exceeding the course requirements.

* **Source:** [Gym Members Exercise Dataset (Kaggle)](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset)
* **Volume:** **20,000 Records** (Rows) & 50+ Features (Columns).
* **Key Variables:**
    * **Categorical:** `Workout_Type`, `Diet_Type`, `Gender`, `Difficulty_Level`.
    * **Numerical:** `Session_Duration`, `Calories_Burned`, `Max_BPM`, `Avg_BPM`, `BMI`.
    * **Derived:** `Fat_Percentage`, `Water_Intake`.

---

## 👥 Team & Roles
The development was structured into three specialized domains, delivering **9 distinct visualizations** (including 4 Advanced types).

| Team Member | Domain | Key Contributions |
| :--- | :--- | :--- |
| **İbrahim Emre Yıldız** | • **System Design:** Built the Streamlit layout, Sidebar Logic, and Data Loading pipeline.<br>• **Sankey Diagram:** Mapped `Diet_Type` → `Workout_Type` flow.<br>• **Treemap:** Hierarchical view of Muscle Groups.<br>• **Bar Chart:** Demographic split analysis. |
| **Kamal Asadov** | • **Multidimensional Analysis:** Developed the Sunburst Chart for `Diet` → `Workout` → `Difficulty` drill-down.<br>• **Correlation:** Scatter plots for `Max_BPM` vs `Avg_BPM`.<br>• **Time-Series:** Heart rate trends by age. |
| **Muhlis Çolak** | • **Density Estimation:** Implemented Density Contours for Age/Gender clustering.<br>• **Outlier Detection:** Box Plots for session duration.<br>• **Distribution:** Histograms for heart rate frequencies. |

---

## ⚙️ Technical Architecture

### Data Processing Pipeline
The application includes a robust preprocessing engine (`load_data` function) that ensures data integrity before visualization:
1.  **Data Loading:** Ingests `Final_data.csv` using Pandas.
2.  **Type Casting:** Converts floating-point age and metric values to integers for cleaner UI display.
3.  **Rounding Logic:** Applies rounding to specific columns (e.g., `Sets`, `Reps`, `BPM`) to reflect realistic fitness metrics.
4.  **Error Handling:** Includes `try-except` blocks to gracefully handle missing dataset files.

### Tech Stack
* **Frontend:** `Streamlit` (Wide-layout optimized)
* **Visualization Engine:** `Plotly Express` & `Plotly Graph Objects`
* **Statistical Backend:** `Statsmodels` (OLS Regression), `NumPy`
* **Data Manipulation:** `Pandas`

---

## 📊 Key Insights
Based on our visual analysis, we derived the following actionable insights:

1.  **Diet Dictates Intensity:**
    * Users on **High-Protein Diets (Paleo, Keto)** significantly cluster around high-intensity workouts like *Strength Training* and *HIIT*.
    * **Vegan/Vegetarian** users show a more balanced distribution, with a slight preference for *Yoga* and *Cardio*.

2.  **The "Experience" Factor:**
    * Scatter analysis reveals that users with higher *Experience Levels* maintain a lower *Average BPM* even during peak intensity sessions, indicating superior cardiovascular efficiency.

3.  **Demographic Hotspots:**
    * The Density Contour plot identifies the **Male, 25-35 Age Group** as the most active demographic, whereas Female participation is more evenly spread across the 20-40 range.

---

## 🚀 Installation Guide

**Step 1: Clone the Repository**
```bash
git clone [https://github.com/IbrahimEmreYildiz/data_visulation_dashboard]
cd [data_visulation_dashboard]
