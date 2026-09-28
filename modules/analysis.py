import pandas as pd


SUBJECTS = [
    "Mathematics",
    "Python",
    "DBMS",
    "Operating Systems",
    "Data Structures"
]


def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B"

    elif percentage >= 60:
        return "C"

    elif percentage >= 50:
        return "D"

    elif percentage >= 40:
        return "E"

    else:
        return "F"


def calculate_result(row):

    for subject in SUBJECTS:

        if row[subject] < 40:
            return "FAIL"

    return "PASS"


def add_analysis_columns(df):

    df = df.copy()

    # Calculate total
    df["Total"] = df[SUBJECTS].sum(axis=1)

    # Calculate percentage
    df["Percentage"] = (
        df["Total"] /
        (len(SUBJECTS) * 100)
    ) * 100

    # Calculate grade
    df["Grade"] = df["Percentage"].apply(
        calculate_grade
    )

    # Calculate result
    df["Result"] = df.apply(
        calculate_result,
        axis=1
    )

    return df


def get_summary(df):

    if len(df) == 0:

        return {
            "students": 0,
            "average": 0,
            "highest": 0,
            "pass_rate": 0
        }

    return {

        "students": len(df),

        "average": df["Percentage"].mean(),

        "highest": df["Percentage"].max(),

        "pass_rate": (
            df["Result"].eq("PASS").mean()
            * 100
        )
    }