import pandas as pd
import altair as alt

from .analysis import SUBJECTS


def subject_average_chart(df):

    data = pd.DataFrame(
        {
            "Subject": SUBJECTS,
            "Average": [
                df[subject].mean()
                for subject in SUBJECTS
            ]
        }
    )

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Subject:N",
                sort="-y",
                title="Subject"
            ),

            y=alt.Y(
                "Average:Q",
                scale=alt.Scale(
                    domain=[0, 100]
                ),
                title="Average Marks"
            ),

            tooltip=[
                "Subject",
                "Average"
            ]
        )
        .properties(
            height=350
        )
    )

    return chart


def grade_distribution_chart(df):

    data = (
        df["Grade"]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        "Grade",
        "Students"
    ]

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Grade:N",
                title="Grade"
            ),

            y=alt.Y(
                "Students:Q",
                title="Number of Students"
            ),

            tooltip=[
                "Grade",
                "Students"
            ]
        )
        .properties(
            height=350
        )
    )

    return chart


def performance_chart(df):

    data = df[
        [
            "Name",
            "Percentage"
        ]
    ].copy()

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Name:N",
                sort="-y",
                title="Student"
            ),

            y=alt.Y(
                "Percentage:Q",
                scale=alt.Scale(
                    domain=[0, 100]
                ),
                title="Percentage"
            ),

            tooltip=[
                "Name",
                "Percentage"
            ]
        )
        .properties(
            height=450
        )
    )

    return chart