import os
import pandas as pd


DATA_FILE = os.path.join(
    "data",
    "students.csv"
)


def load_data():

    return pd.read_csv(
        DATA_FILE
    )


def save_data(df):

    columns = [
        "Roll No",
        "Name",
        "Mathematics",
        "Python",
        "DBMS",
        "Operating Systems",
        "Data Structures"
    ]

    base = df[columns].copy()

    base.to_csv(
        DATA_FILE,
        index=False
    )


def add_student(df, student):

    return pd.concat(
        [
            df,
            pd.DataFrame([student])
        ],
        ignore_index=True
    )


def delete_student(df, roll_no):

    return df[
        df["Roll No"].astype(str)
        != str(roll_no)
    ].copy()