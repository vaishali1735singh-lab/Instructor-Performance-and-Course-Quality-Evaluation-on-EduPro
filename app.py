import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="📚",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    teachers = pd.read_excel("Book 8.xlsx", sheet_name="Sheet1")
    courses = pd.read_excel("Book 8.xlsx", sheet_name="Sheet2")
    return teachers, courses

teachers, courses = load_data()

# Dashboard Title
st.title("📚 EduPro Dashboard")
st.subheader("Instructor Performance and Course Quality Evaluation")

st.sidebar.header("🔎 Dashboard Filters")

# Teacher Filters
gender = st.sidebar.multiselect(
    "Select Gender",
    teachers["Gender"].unique(),
    default=teachers["Gender"].unique()
)

expertise = st.sidebar.multiselect(
    "Select Expertise",
    teachers["Expertise"].unique(),
    default=teachers["Expertise"].unique()
)

rating_range = st.sidebar.slider(
    "Teacher Rating Range",
    float(teachers["Teacher Rating"].min()),
    float(teachers["Teacher Rating"].max()),
    (
        float(teachers["Teacher Rating"].min()),
        float(teachers["Teacher Rating"].max())
    )
)

# Course Filters
category = st.sidebar.multiselect(
    "Select Course Category",
    courses["Course Category"].unique(),
    default=courses["Course Category"].unique()
)

level = st.sidebar.multiselect(
    "Select Course Level",
    courses["Course Level"].unique(),
    default=courses["Course Level"].unique()
)

# Apply Teacher Filters
filtered_teachers = teachers[
    (teachers["Gender"].isin(gender)) &
    (teachers["Expertise"].isin(expertise)) &
    (teachers["Teacher Rating"] >= rating_range[0]) &
    (teachers["Teacher Rating"] <= rating_range[1])
]

# Apply Course Filters
filtered_courses = courses[
    (courses["Course Category"].isin(category)) &
    (courses["Course Level"].isin(level))
]

# KPI Section
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Teacher Rating",
    round(filtered_teachers["Teacher Rating"].mean(), 2)
)

col2.metric(
    "Average Course Rating",
    round(filtered_courses["Course Rating"].mean(), 2)
)

col3.metric(
    "Average Teaching Experience",
    round(filtered_teachers["Years of Experience"].mean(), 2)
)

col4.metric(
    "Highest Teacher Rating",
    filtered_teachers["Teacher Rating"].max()
)

st.divider()

# Instructor Leaderboard
st.subheader("🏆 Instructor Performance Leaderboard")

leaderboard = filtered_teachers[
    ["Teacher Name", "Expertise", "Years of Experience", "Teacher Rating"]
].sort_values(by="Teacher Rating", ascending=False)

st.dataframe(leaderboard, use_container_width=True)

# Expertise-wise Performance
st.subheader("📚 Expertise-wise Performance")

expertise_rating = filtered_teachers.groupby(
    "Expertise"
)["Teacher Rating"].mean().reset_index()

fig1 = px.bar(
    expertise_rating,
    x="Expertise",
    y="Teacher Rating",
    title="Average Teacher Rating by Expertise"
)

st.plotly_chart(fig1, use_container_width=True)

# Experience vs Rating
st.subheader("📈 Experience vs Teacher Rating")

fig2 = px.scatter(
    filtered_teachers,
    x="Years of Experience",
    y="Teacher Rating",
    color="Gender",
    hover_data=["Teacher Name", "Expertise"],
    title="Teaching Experience vs Teacher Rating"
)

st.plotly_chart(fig2, use_container_width=True)

# Gender-wise Analysis
st.subheader("👨‍🏫👩‍🏫 Gender-wise Performance")

gender_rating = filtered_teachers.groupby(
    "Gender"
)["Teacher Rating"].mean().reset_index()

fig3 = px.bar(
    gender_rating,
    x="Gender",
    y="Teacher Rating",
    title="Average Teacher Rating by Gender"
)

st.plotly_chart(fig3, use_container_width=True)

# Course Category Analysis
st.subheader("📖 Course Category Analysis")

category_rating = filtered_courses.groupby(
    "Course Category"
)["Course Rating"].mean().reset_index()

fig4 = px.bar(
    category_rating,
    x="Course Category",
    y="Course Rating",
    title="Average Course Rating by Category"
)

st.plotly_chart(fig4, use_container_width=True)

# Course Level Analysis
st.subheader("🎓 Course Level Analysis")

level_rating = filtered_courses.groupby(
    "Course Level"
)["Course Rating"].mean().reset_index()

fig5 = px.bar(
    level_rating,
    x="Course Level",
    y="Course Rating",
    title="Average Course Rating by Level"
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

st.markdown("### 📌 EduPro Education Analytics Dashboard")
st.markdown("Business Analytics Project | Instructor Performance & Course Quality Evaluation")
