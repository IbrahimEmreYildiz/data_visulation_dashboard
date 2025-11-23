# 🏋️ Gym & Fitness Lifestyle Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

> **CEN445 - Introduction to Data Visualization Course Project**

## 📖 Project Overview
This interactive dashboard is designed to analyze the complex relationships between **lifestyle habits, nutritional intake, and physiological health**. Utilizing a large-scale dataset of **20,000 records**, the application visualizes how specific diet types influence workout intensity, tracks demographic health trends, and identifies correlations between heart rate efficiency and exercise experience.

The dashboard leverages **Streamlit** for interactivity and **Plotly** for advanced, dynamic visualizations, offering users a deep dive into fitness analytics.

## 📂 Dataset Information
* **Dataset Name:** Gym Members Exercise Dataset
* **Source:** [Kaggle Link](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset)
* **Scale:** **20,000 Rows** (Significantly exceeds the course requirement of 2,000 rows).
* **Key Attributes:** `Workout_Type`, `Session_Duration`, `Calories_Burned`, `BMI`, `Max_BPM`, `Avg_BPM`, `Diet_Type`, `Fat_Percentage`, `Water_Intake`.

## ✨ Key Features
* **Interactive Filtering:** Sidebar controls to filter data by Gender, Workout Type, Diet, and Difficulty Level.
* **Advanced Visualizations:** Includes Sankey Diagrams, Sunburst Charts, Treemaps, and Density Contours.
* **Data-Driven Insights:** Real-time calculation of trends based on user selection.
* **Responsive Design:** Optimized layout using Streamlit's wide mode.

---

## 🏗️ Project Structure
```bash
├── dashboard.py           # Main application file (Streamlit App)
├── Final_data.csv         # Processed Dataset (20k rows)
├── requirements.txt       # Project dependencies
├── README.md              # Project Documentation
└── .gitignore             # Git ignore file

