import streamlit as st
import pandas as pd

from modules.analysis import add_analysis_columns, get_summary
from modules.data_manager import load_data, save_data, delete_student
from modules.charts import (
    subject_average_chart,
    grade_distribution_chart,
    performance_chart
)


st.set_page_config(
    page_title="Student Marks Analysis",
    page_icon="🎓",
    layout="wide"
)


st.title("🎓 Student Marks Analysis System")
st.caption("Academic Performance Analysis Dashboard")


try:
    df = load_data()
    df = add_analysis_columns(df)
except Exception as e:
    st.error("Error loading student data.")
    st.exception(e)
    st.stop()

subjects = [
    "Mathematics",
    "Python",
    "DBMS",
    "Operating Systems",
    "Data Structures"
]

# Sidebar
st.sidebar.title("📌 Menu")

page = st.sidebar.radio(
    "Select Page",
    [
        "📊 Dashboard",
        "👨‍🎓 Student Records",
        "📑 Student Report",
        "ℹ️ About"
    ]
)


if page == "📊 Dashboard":

    st.header("📊 Performance Dashboard")

    summary = get_summary(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Total Students",
        summary["students"]
    )

    col2.metric(
        "📊 Class Average",
        f"{summary['average']:.2f}%"
    )

    col3.metric(
        "🏆 Highest Score",
        f"{summary['highest']:.2f}%"
    )

    col4.metric(
        "✅ Pass Rate",
        f"{summary['pass_rate']:.1f}%"
    )

    st.divider()

    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Subject-wise Average")

        chart = subject_average_chart(df)

        st.altair_chart(
            chart,
            use_container_width=True
        )

    with col2:
        st.subheader("🎯 Grade Distribution")

        chart = grade_distribution_chart(df)

        st.altair_chart(
            chart,
            use_container_width=True
        )

    st.subheader("📈 Student Performance")

    chart = performance_chart(df)

    st.altair_chart(
        chart,
        use_container_width=True
    )

    # Top students
    st.subheader("🏆 Top 10 Students")

    top_students = df.sort_values(
        "Percentage",
        ascending=False
    ).head(10)

    st.dataframe(
        top_students[
            [
                "Roll No",
                "Name",
                "Total",
                "Percentage",
                "Grade",
                "Result"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )



elif page == "👨‍🎓 Student Records":

    st.header("👨‍🎓 Student Records")

    # Add student
    with st.expander("➕ Add New Student"):

        with st.form("student_form"):

            roll = st.text_input("Roll Number")

            name = st.text_input("Student Name")

            st.subheader("Enter Marks")

            col1, col2 = st.columns(2)

            with col1:

                mathematics = st.number_input(
                    "Mathematics",
                    min_value=0,
                    max_value=100,
                    value=50
                )

                python_marks = st.number_input(
                    "Python",
                    min_value=0,
                    max_value=100,
                    value=50
                )

                dbms = st.number_input(
                    "DBMS",
                    min_value=0,
                    max_value=100,
                    value=50
                )

            with col2:

                operating_systems = st.number_input(
                    "Operating Systems",
                    min_value=0,
                    max_value=100,
                    value=50
                )

                data_structures = st.number_input(
                    "Data Structures",
                    min_value=0,
                    max_value=100,
                    value=50
                )

            submitted = st.form_submit_button(
                "➕ Add Student"
            )

            if submitted:

                if not roll.strip():
                    st.error("Please enter Roll Number.")

                elif not name.strip():
                    st.error("Please enter Student Name.")

                elif roll in df["Roll No"].astype(str).values:
                    st.error("Roll Number already exists.")

                else:

                    new_student = {
                        "Roll No": roll,
                        "Name": name,
                        "Mathematics": mathematics,
                        "Python": python_marks,
                        "DBMS": dbms,
                        "Operating Systems": operating_systems,
                        "Data Structures": data_structures
                    }

                    base_columns = [
                        "Roll No",
                        "Name",
                        "Mathematics",
                        "Python",
                        "DBMS",
                        "Operating Systems",
                        "Data Structures"
                    ]

                    new_df = pd.concat(
                        [
                            df[base_columns],
                            pd.DataFrame([new_student])
                        ],
                        ignore_index=True
                    )

                    save_data(new_df)

                    st.success(
                        "✅ Student added successfully!"
                    )

                    st.rerun()

    st.divider()

    st.subheader("🔍 Search Students")

    search = st.text_input(
        "Search by name or roll number"
    )

    display_df = df.copy()

    if search:

        display_df = display_df[
            display_df["Name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
            |
            display_df["Roll No"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        display_df[
            [
                "Roll No",
                "Name",
                "Mathematics",
                "Python",
                "DBMS",
                "Operating Systems",
                "Data Structures",
                "Total",
                "Percentage",
                "Grade",
                "Result"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Delete student
    st.subheader("🗑️ Delete Student")

    roll_delete = st.selectbox(
        "Select Roll Number",
        [""] + df["Roll No"].astype(str).tolist()
    )

    if st.button("🗑️ Delete Selected Student"):

        if not roll_delete:

            st.warning("Please select a student.")

        else:

            df = delete_student(
                df,
                roll_delete
            )

            save_data(df)

            st.success(
                "Student deleted successfully."
            )

            st.rerun()

    st.divider()

    # Download CSV
    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Student Data",
        csv_data,
        "student_analysis.csv",
        "text/csv"
    )




elif page == "📑 Student Report":

    st.header("📑 Individual Student Report")

    roll_numbers = (
        df["Roll No"]
        .astype(str)
        .tolist()
    )

    selected_roll = st.selectbox(
        "Select Student",
        roll_numbers
    )

    student = df[
        df["Roll No"].astype(str)
        == selected_roll
    ].iloc[0]

    st.subheader(
        f"👨‍🎓 {student['Name']}"
    )

    st.write(
        f"**Roll Number:** {student['Roll No']}"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Marks",
        int(student["Total"])
    )

    col2.metric(
        "Percentage",
        f"{student['Percentage']:.2f}%"
    )

    col3.metric(
        "Grade",
        student["Grade"]
    )

    col4.metric(
        "Result",
        student["Result"]
    )

    st.divider()

    report = pd.DataFrame(
        {
            "Subject": subjects,
            "Marks": [
                student[subject]
                for subject in subjects
            ]
        }
    )

    st.subheader("📚 Subject Performance")

    st.bar_chart(
        report.set_index("Subject")
    )

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    if student["Result"] == "PASS":

        st.success(
            "🎉 Student has passed all subjects."
        )

    else:

        st.error(
            "⚠️ Student has failed one or more subjects."
        )



elif page == "ℹ️ About":

    st.header("ℹ️ About Project")

    st.markdown(
        """
        ## 🎓 Student Marks Analysis System

        This project is developed using Python and
        Streamlit to analyze student academic performance.

        ### Technologies

        - Python
        - Pandas
        - Streamlit
        - Altair
        - CSV

        ### Features

        - Student record management
        - Add students
        - Delete students
        - Search students
        - Total marks calculation
        - Percentage calculation
        - Grade calculation
        - Pass/Fail analysis
        - Subject-wise analysis
        - Interactive charts
        - Top student analysis
        - Individual student reports
        - CSV download
        """
    )